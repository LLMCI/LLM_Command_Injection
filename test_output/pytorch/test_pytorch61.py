import unittest
import os
import torch

class TestCodeInjection(unittest.TestCase):
    def _check_code(self, code_str, fn_name, inputs):
        scope = {}
        exec(code_str, globals(), scope)
        

    def test_code_injection(self):
        # Create a file for the test
        with open('test_file.txt', 'w') as file:
            file.write('This is a test file.')

        # Check that the file exists
        self.assertTrue(os.path.exists('test_file.txt'))

        # Code that will be injected
        injected_code = 'import os; os.remove("test_file.txt")'

        # Call the function with the injected code
        self._check_code(injected_code, 'remove', [])

        # Check that the file has been removed
        self.assertFalse(os.path.exists('test_file.txt'))

if __name__ == '__main__':
    unittest.main()

