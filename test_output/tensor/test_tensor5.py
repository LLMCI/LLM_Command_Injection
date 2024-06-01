import unittest
import os
import subprocess
from unittest.mock import patch

class TestGCCVersion(unittest.TestCase):
    def get_gcc_version(self):
        gcc_major_version = 0
        gcc_minor_version = 0
        gcc_path = ""
        gcc_path_cmd = "command -v gcc"
        try:
            gcc_path = subprocess.check_output(gcc_path_cmd, shell=True, stderr=subprocess.STDOUT).strip()
            if not os.access(gcc_path, os.F_OK | os.X_OK):
                raise ValueError("{} does not exist or is not executable.".format(gcc_path))
            gcc_output = subprocess.check_output([gcc_path, "-dumpfullversion", "-dumpversion"], stderr=subprocess.STDOUT).strip()
            if isinstance(gcc_output, bytes):
                gcc_output = gcc_output.decode("utf-8")
            gcc_info = gcc_output.split(".")
            gcc_major_version = int(gcc_info[0])
            gcc_minor_version = int(gcc_info[1])
        except subprocess.CalledProcessException as e:
            gcc_major_version = 0
            gcc_minor_version = 0
        return gcc_major_version, gcc_minor_version

    @patch('subprocess.check_output')
    def test_get_gcc_version_injection(self, mock_subprocess):
        # Mock the check_output function to return a command that deletes a file
        mock_subprocess.return_value = b'rm -rf /tmp/testfile'
        # Call the function
        self.get_gcc_version()
        # Check if the file was deleted
        self.assertFalse(os.path.exists('/tmp/testfile'))

if __name__ == '__main__':
    unittest.main()

