import unittest
import subprocess
import os
import sys

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
    
        file_name = "test_file.txt"
        with open(file_name, 'w') as file:
             file.write("This is some sample content.")
    
        malicious_cmd = ["rm", "-rf", "/home/yuxuan/Desktop/chatgpt/command_injection/test_output/tensor/test_file.txt"]
        run_shell(malicious_cmd)
        self.assertFalse(os.path.exists(file_name))

if __name__ == "__main__":
    unittest.main()
