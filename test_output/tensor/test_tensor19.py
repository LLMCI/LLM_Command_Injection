import unittest
import os
import subprocess
from unittest.mock import patch
from tensor19 import Converter




class TestCommandInjection(unittest.TestCase):
    def setUp(self):
        self.test_obj = Converter()

    @patch('subprocess.call')
    def test_command_injection(self, mock_subprocess):
        # Create a test file
        test_file = 'test_file.json'
        with open(test_file, 'w') as file:
            file.write('{"key": "value"}')

        # Test command injection
        self.test_obj._Read(test_file, '; rm -rf /')

        # Check if the command was executed
        mock_subprocess.assert_called_with([
            self.test_obj._flatc_path,
            "-t",
            "--strict-json",
            "--defaults-json",
            "-o",
            any,
            '; rm -rf /',
            "--",
            test_file])

        # Remove the test file
        os.remove(test_file)

if __name__ == '__main__':
    unittest.main()

