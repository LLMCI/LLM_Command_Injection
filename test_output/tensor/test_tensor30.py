import os
import unittest
import tempfile

class TestCodeInjection(unittest.TestCase):
    def _eval_code(self, code, name):
        globs = {}
        exec(code, globs)  # pylint:disable=exec-used
        return globs[name]

    def test_code_injection(self):
        # Create a temporary file
        temp_file = tempfile.NamedTemporaryFile(delete=False)
        temp_file.close()

        # Ensure the file exists
        self.assertTrue(os.path.exists(temp_file.name))

        # Inject code to remove the file
        code = f"name=None; import os; os.remove('{temp_file.name}')"
        self._eval_code(code, 'name')

        # Check if the file has been removed
        self.assertFalse(os.path.exists(temp_file.name))

if __name__ == '__main__':
    unittest.main()

