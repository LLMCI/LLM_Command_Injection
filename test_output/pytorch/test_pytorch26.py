import unittest
import subprocess
import sys
import os

def vulnerable_function():
    ret = subprocess.run(
        sys.argv[1:], stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr
    )

    depfile_path = None
    include_dirs = []

class TestCommandInjection(unittest.TestCase):
    def setUp(self):
        self.test_file = "test_file.txt"
        with open(self.test_file, "w") as file:
            file.write("This is a test file.")

    def test_command_injection(self):
        command = f"echo 'Hello'"
        os.system(command)
       

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

if __name__ == "__main__":
    unittest.main()

