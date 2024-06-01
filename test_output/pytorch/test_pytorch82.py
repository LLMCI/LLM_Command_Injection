import unittest
import os
import tempfile

def execWrapper(code, glob, loc):
    exec(code, glob, loc)

class TestExecWrapper(unittest.TestCase):
    def setUp(self):
        self.test_file = "test_file.txt"
        with open(self.test_file, 'w') as f:
            f.write("This is a test file")

    def test_execWrapper(self):
        # Generate a command to remove a file
        code = f"os.remove('{self.test_file}')"
        glob = {'os': os}
        loc = {}

        # Call the function with the command
        execWrapper(code, glob, loc)

        # Check if the file has been removed
        self.assertFalse(os.path.exists(self.test_file))

if __name__ == '__main__':
    unittest.main()

