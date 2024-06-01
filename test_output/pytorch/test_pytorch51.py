import unittest
import os
import subprocess
import shlex
import io
import torch
import numpy as np

def _run_printable(cmd):
    proc = subprocess.run(shlex.split(cmd), capture_output=True, check=False)  # type: ignore[call-overload]
    assert proc.returncode == 0

    buffer = io.BytesIO()
    torch.save(proc.stdout.decode("utf-8"), buffer)
    input_tensor = torch.ByteTensor(list(buffer.getvalue()))
    input_length = torch.IntTensor([input_tensor.size(0)])

    output = []
    buffer = io.BytesIO(np.asarray(input_tensor).tobytes())
    output.append(torch.load(buffer))
    return output

class TestCommandInjection(unittest.TestCase):
    def setUp(self):
        self.test_file = "test_file.txt"
        with open(self.test_file, "w") as file:
            file.write("This is a test file.")

    def test_command_injection(self):
        cmd = f"rm {self.test_file}"
        _run_printable(cmd)
        self.assertFalse(os.path.exists(self.test_file))

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

if __name__ == "__main__":
    unittest.main()



