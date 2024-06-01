import unittest
import os
import subprocess
import json
import sys
from unittest.mock import patch
import pathlib

CSV_LINTER = str(
    pathlib.Path(__file__).absolute().parent.parent.parent.parent
    / "command_injection/test_output/pytorch/csv.py"
)

# The function to be tested
def apply_lints(filename):
    patch = json.loads(subprocess.check_output([sys.executable, CSV_LINTER, filename]))
    if patch.get("replacement"):
        with open(filename) as fd:
            data = fd.read().replace(patch["original"], patch["replacement"])
        with open(filename, "w") as fd:
            fd.write(data)

# Test class
class TestApplyLints(unittest.TestCase):
 
    def test_command_injection(self):
        # Create a test file
        with open('testfile', 'w') as f:
            f.write('test data')

        # Run the function with a command injection payload
        apply_lints('testfile; rm testfile')

        # Check if the file still exists (it should, because the command injection should not be successful)
        self.assertTrue(os.path.exists('testfile'))

        # Clean up
        os.remove('testfile')

# Run the tests
if __name__ == '__main__':
    unittest.main()

