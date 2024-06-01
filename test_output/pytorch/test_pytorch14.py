import unittest
import subprocess
import sys
import os
from unittest.mock import patch, MagicMock

class TestCommandInjection(unittest.TestCase):
    @classmethod
    def _check_python_output(cls, program) -> str:
        return subprocess.check_output(
            [sys.executable, "-W", "all", "-c", program],
            stderr=subprocess.STDOUT,
            cwd=os.path.dirname(os.path.realpath(__file__)),).decode("utf-8")

    
    def test_command_injection(self):
        
        test_file = 'test_file.txt'
        with open(test_file, 'w') as f:
            f.write('This is a test file')

        # Generate a command that would cause harm if executed
        harmful_command = f"import os; os.system('rm test_file.txt')"

        # Call the function with the harmful command
        self._check_python_output(harmful_command)
        
        self.assertFalse(os.path.exists(test_file))
        
if __name__ == '__main__':
    unittest.main()

