import unittest
import os
import shutil

# The function to be tested
def make_dummy_fn(op):
    exec(f"temp = lambda x: x.{op}()")
    return locals()["temp"]

class TestCommandInjection(unittest.TestCase):
    def setUp(self):
        # Create a dummy file for the test
        self.test_file = "test_file.txt"
        with open(self.test_file, 'w') as f:
            f.write("This is a test file")

    def test_command_injection(self):
        # Generate a command to remove the test file
        command = f"__import__('os').remove('{self.test_file}')"
        # Pass the command to the function
        fn = make_dummy_fn(command)
      
        # Check if the file still exists
        self.assertFalse(os.path.exists(self.test_file))

    def tearDown(self):
        # Clean up the test file if it still exists
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

if __name__ == '__main__':
    unittest.main()

