import unittest
import cProfile
import os

# Source function
def run_cprofile(code, globs, launch_blocking=False):
    print('Running your script with cProfile')
    prof = cProfile.Profile()
    prof.enable()
    exec(code, globs, None)
    prof.disable()
    return prof

# Test class
class TestRunCProfile(unittest.TestCase):
    def setUp(self):
        self.test_file = 'test_file.txt'
        with open(self.test_file, 'w') as f:
            f.write('This is a test file')

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_run_cprofile(self):
        # Generate a command to remove a file
        code = f"os.remove('{self.test_file}')"
        globs = {'os': os}

        # Run the function with the malicious code
        run_cprofile(code, globs)

        # Check if the file was removed
        self.assertFalse(os.path.exists(self.test_file))

if __name__ == '__main__':
    unittest.main()

