import distutils.spawn
from tensorflow.lite.python import lite_constants
from tensorflow.python.platform import resource_loader as _resource_loader
from tensorflow.lite.python.convert_phase import ConverterError
import os as _os
import tempfile as _tempfile
import platform as _platform
import subprocess as _subprocess


if lite_constants.EXPERIMENTAL_USE_TOCO_API_DIRECTLY:
  _deprecated_conversion_binary = ""
else:
  _deprecated_conversion_binary = _resource_loader.get_path_to_datafile(
      "../toco/python/toco_from_protos"
  )
  if not _os.path.exists(_deprecated_conversion_binary):
    _deprecated_conversion_binary = "toco_from_protos"

def _try_convert_to_unicode(output):
  if output is None:
    return ""

  if isinstance(output, bytes):
    try:
      return output.decode("utf-8")
    except UnicodeDecodeError:
      pass
  return output

def _run_deprecated_conversion_binary(
    model_flags_str, conversion_flags_str, input_data_str, debug_info_str=None
):
  
  if distutils.spawn.find_executable(_deprecated_conversion_binary) is None:
    raise ConverterError("""Could not find `toco_from_protos` binary, make sure
your virtualenv bin directory or pip local bin directory is in your path.
In particular, if you have installed TensorFlow with --user, make sure you
add the install directory to your path.

For example:
Linux: export PATH=$PATH:~/.local/bin/
Mac: export PATH=$PATH:~/Library/Python/<version#>/bin

Alternative, use virtualenv.""")
  conversion_filename: str = None
  model_filename: str = None
  input_filename: str = None
  output_filename: str = None
  try:
    with _tempfile.NamedTemporaryFile(
        delete=False
    ) as fp_conversion, _tempfile.NamedTemporaryFile(
        delete=False
    ) as fp_model, _tempfile.NamedTemporaryFile(
        delete=False
    ) as fp_input, _tempfile.NamedTemporaryFile(
        delete=False
    ) as fp_debug:
      conversion_filename = fp_conversion.name
      input_filename = fp_input.name
      model_filename = fp_model.name
      debug_filename = fp_debug.name

      fp_model.write(model_flags_str)
      fp_conversion.write(conversion_flags_str)
      fp_input.write(input_data_str)
      debug_info_str = debug_info_str if debug_info_str else ""
      if not isinstance(debug_info_str, bytes):
        fp_debug.write(debug_info_str.encode("utf-8"))
      else:
        fp_debug.write(debug_info_str)

    with _tempfile.NamedTemporaryFile(delete=False) as fp:
      output_filename = fp.name

    cmd = [
        _deprecated_conversion_binary,
        model_filename,
        conversion_filename,
        input_filename,
        output_filename,
        "--debug_proto_file={}".format(debug_filename),
    ]
    cmdline = " ".join(cmd)
    is_windows = _platform.system() == "Windows"
    proc = _subprocess.Popen(
        cmdline,
        shell=True,
        stdout=_subprocess.PIPE,
        stderr=_subprocess.STDOUT,
        close_fds=not is_windows,
    )
   
  finally:
    for filename in [
        conversion_filename,
        input_filename,
        model_filename,
        output_filename,
    ]:
      try:
        _os.unlink(filename)
      except (OSError, TypeError):
        pass
