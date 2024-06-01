import unittest
import subprocess
import os
import locale

def run(command):
    """Return (return-code, stdout, stderr)."""
    shell = True if type(command) is str else False
    p = subprocess.Popen(command, stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE, shell=shell)
    raw_output, raw_err = p.communicate()
    rc = p.returncode
    

class TestRun(unittest.TestCase):
    def test_command_injection(self):
        # Create a test file
        with open('test_file.txt', 'w') as f:
            f.write('This is a test file.')

        # Command injection payload
        payload = 'echo hello; rm test_file.txt'

        # Run the command
        run(payload)

        # Check if the file was removed
        self.assertFalse(os.path.exists('test_file.txt'))

if __name__ == '__main__':
    unittest.main()

