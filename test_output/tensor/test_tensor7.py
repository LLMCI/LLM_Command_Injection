import unittest
import os
import subprocess

class TestCommandInjection(unittest.TestCase):
    def test_func_wo_source_code(self):
        code = "def f_exec():\n  os.system('rm -rf /tmp/test_file')"
        exec(code, globals())  # pylint: disable=exec-used

        # Create a test file
        with open('/tmp/test_file', 'w') as file:
            file.write('This is a test file.')

        # Call the function
        f_exec()  # pylint: disable=undefined-variable

        # Check if the file is removed
        self.assertFalse(os.path.exists('/tmp/test_file'))

    def test_func_wo_source_code_injection(self):
        code = "def f_exec(cmd):\n  os.system(cmd)"
        exec(code, globals())  # pylint: disable=exec-used

        # Create a test file
        with open('/tmp/test_file', 'w') as file:
            file.write('This is a test file.')

        # Call the function with a command injection
        f_exec('rm -rf /tmp/test_file')  # pylint: disable=undefined-variable

        # Check if the file is removed
        self.assertFalse(os.path.exists('/tmp/test_file'))

if __name__ == '__main__':
    unittest.main()

