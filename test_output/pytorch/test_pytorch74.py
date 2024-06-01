import unittest
import os
import tempfile

class TestCodeInjection(unittest.TestCase):
    def _test_code(self, code, global_inputs=None):
        if code is not None:
            expr = compile(code, "test", "exec")
            exec(expr, global_inputs)

    def test_code_injection(self):
        # Create a temporary file
        test_file = "test_file.txt"
        with open(test_file, 'w') as f:
            f.write("This is a test file")

        # Ensure the file exists
        self.assertTrue(os.path.exists(test_file))

        # Inject a command to remove the file
        self._test_code(f"os.remove('{test_file}')", {"os": os})

        # Check if the file has been removed
        self.assertFalse(os.path.exists(test_file))

if __name__ == '__main__':
    unittest.main()

