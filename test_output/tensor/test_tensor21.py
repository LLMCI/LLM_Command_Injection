import unittest
import subprocess
import sys
import os

def run_shell(cmd, allow_non_zero=False, stderr=None):
  if stderr is None:
    stderr = sys.stdout
  if allow_non_zero:
    try:
      output = subprocess.check_output(cmd, stderr=stderr)
    except subprocess.CalledProcessError as e:
      output = e.output
  else:
    output = subprocess.check_output(cmd, stderr=stderr)
  return output.decode('UTF-8').strip()

class TestRunShell(unittest.TestCase):

    def test_command_injection(self):  
      
        test_file = "testfile.txt"
        with open(test_file, "w") as file:
            file.write("This is a test file")
            
        # Command injection payload
        payload = ["rm", "-rf", "testfile.txt"]
        run_shell(payload, allow_non_zero=True)
        # Check if the file was removed
        self.assertFalse(os.path.exists(test_file))


if __name__ == "__main__":
    unittest.main()
