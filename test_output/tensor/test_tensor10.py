import unittest
import os
import subprocess

# The function to be tested
def exec_test_function(code):
    # pylint: disable=exec-used
    exec('computed' + code + 'stuff', globals(), locals())

class TestCommandInjection(unittest.TestCase):
    def setUp(self):
        # Create a dummy file for the test
        self.test_file = "test_file.txt"
        with open(self.test_file, 'w') as file:
            file.write("This is a test file")

    def test_exec_test_function(self):
        # Generate a command to remove the test file
        command = "; os.remove(test_file.txt); #"
        exec_test_function(command)

        # Check if the command is executed and the file is removed
        self.assertFalse(os.path.exists(self.test_file))

    def tearDown(self):
        # Clean up the test file if it still exists
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

if __name__ == '__main__':
    unittest.main()
