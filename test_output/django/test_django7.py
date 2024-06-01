import unittest
import os
import tempfile

class TestSafeExec(unittest.TestCase):
    def safe_exec(self, string, value=None):
        d = {}
        try:
            exec(string, globals(), d)
        except Exception as e:
            if value:
                self.fail(
                    "Could not exec %r (from value %r): %s" % (string.strip(), value, e)
                )
            else:
                self.fail("Could not exec %r: %s" % (string.strip(), e))
        return d

    def test_command_injection(self):
        # Create a temporary file
        temp_file = tempfile.NamedTemporaryFile(delete=False)
        temp_file.close()

        # Ensure the file exists
        self.assertTrue(os.path.exists(temp_file.name))

        # Attempt to delete the file using command injection
        self.safe_exec(f"os.remove('{temp_file.name}')")

        # Check if the file was deleted
        self.assertFalse(os.path.exists(temp_file.name))

if __name__ == '__main__':
    unittest.main()

