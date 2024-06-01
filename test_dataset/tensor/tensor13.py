import os
import subprocess
import tempfile
from typing import Any, Sequence

class Runner:
  """Python helper for running Xla runtime runner tools."""

  def __init__(self, runner: str):
    self.runner = runner

  def execute(self,
              module: str,
              function: str,
              arguments: Sequence[Any],
              inout: Sequence[int] = None) -> Sequence[Any]:
    """Executes `module` with user-provided arguments."""
    temp = tempfile.mkdtemp()

    # Write input mlir module to a file.
    module_file = os.path.join(temp, "module.mlir")
    with open(module_file, "w") as f:
      f.write(module)

    inout = set(inout or [])

    # Pack arguments into a proto message.
    args_proto = runner_pb2.ArgumentsProto()
    for i, arg in enumerate(arguments):
      if isinstance(arg, int):
        args_proto.arguments.append(
            runner_pb2.ArgumentProto(scalar=runner_pb2.ScalarProto(i32=arg)))
        if i in inout:
          raise RuntimeError(f"inout param {i} cannot be of type ScalarArg")
        continue
      elif isinstance(arg, np.ndarray):
        element_type = DTYPE_TO_XLA_ELEMENT_TYPE[str(arg.dtype)]
        args_proto.arguments.append(
            runner_pb2.ArgumentProto(
                tensor=runner_pb2.TensorProto(
                    dtype=element_type,
                    sizes=arg.shape,
                    strides=arg.strides,
                    inout=(i in inout),
                    contents=arg.tobytes())))

        continue

      raise TypeError("Unsupported argument type")

    # Serialize argument proto message to a file.
    arguments_file = os.path.join(temp, "arguments.pb")
    with open(arguments_file, "wb") as f:
      f.write(args_proto.SerializeToString())

    # Expected results file path.
    results_file = os.path.join(temp, "results.pb")

    # Execute the runner tool.
    runner_cmd = [
        self.runner, "--logtostderr", f"--function={function}",
        f"--module={module_file}", f"--arguments={arguments_file}",
        f"--results={results_file}"
    ]
    result = subprocess.run(runner_cmd, capture_output=False, check=False)

    if result.returncode != 0:
      err = result.stderr.decode("utf-8")
      raise RuntimeError(f"failed to execute runner tool: {err}")

    # Read returned results.
    with open(results_file, "rb") as f:
      results_proto = runner_pb2.ResultsProto.FromString(f.read())

    # Convert results from proto back to python objects.
    results = []

    for res in results_proto.results:
      # Convert ScalarProto to scalar object
      if res.HasField("scalar"):
        scalar = res.scalar

        if hasattr(scalar, "i32"):
          results.append(scalar.i32)
          continue
        if hasattr(scalar, "i64"):
          results.append(scalar.i64)
          continue

      # Convert TensorProto to numpy array
      elif res.HasField("tensor"):
        tensor = res.tensor
        dtype = XLA_ELEMENT_TYPE_TO_DTYPE[tensor.dtype]
        result_array = np.frombuffer(tensor.contents, dtype=dtype)
        results.append(result_array)
        continue

      raise ValueError(f"Unknown result {res}")

    return results
