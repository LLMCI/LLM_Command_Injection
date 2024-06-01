import unittest
import os
import subprocess
from typing import List, Any, Tuple

# Source function
def run(args: List[str], **kwargs: Any) -> Tuple[subprocess.CompletedProcess, str]:
    stdout_stderr_log = "log.txt"
    f_stdout_stderr = open(stdout_stderr_log, "wb")
    try:
        invocation = subprocess.run(
            args,
            stdout=f_stdout_stderr,
            stderr=subprocess.STDOUT,
            **kwargs,
        )
        with open(stdout_stderr_log) as f:
            return invocation, f.read()
    finally:
        f_stdout_stderr.close()

# Test class
class TestRun(unittest.TestCase):
    def setUp(self):
        self.test_file = "test_file.txt"
        with open(self.test_file, "w") as f:
            f.write("This is a test file.")

    def test_run(self):
        # Generate a command that removes a file
        command = ["rm", self.test_file]
        run(command)
        # Check if the command is executed
        self.assertFalse(os.path.exists(self.test_file))
        
    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

if __name__ == "__main__":
    unittest.main()

