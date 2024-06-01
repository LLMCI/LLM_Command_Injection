import unittest
import os
import sys
import subprocess

def run_process_no_exception(code, env=None):
    popen = subprocess.Popen(
        [sys.executable, '-c', code],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env=env)
    (stdout, stderr) = popen.communicate()
    return (stdout, stderr)

class TestRunProcessNoException(unittest.TestCase):
    def setUp(self):
        self.test_file = 'test_file.txt'
        with open(self.test_file, 'w') as file:
            file.write('This is a test file')

    def test_command_injection(self):
        # Command to remove the test file
        command = f'import os; os.remove("{self.test_file}")'
        run_process_no_exception(command)

        # Check if the file has been removed
        self.assertFalse(os.path.exists(self.test_file))

    def tearDown(self):
        # Clean up any leftover test file
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

if __name__ == '__main__':
    unittest.main()

