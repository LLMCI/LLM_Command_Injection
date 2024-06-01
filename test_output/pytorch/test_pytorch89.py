import unittest
import os
import subprocess
from unittest.mock import patch

def GetSymbolTrie(target, nm_command, max_depth):
    # Run nm to get a dump on the strings.
    proc = subprocess.Popen(
        [nm_command, '--radix=d', '--size-sort', '--print-size', target],
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    

class TestGetSymbolTrie(unittest.TestCase):
    def test_command_injection(self):
        with open('test_file.txt', 'w') as f:
            f.write('This is a test file.')
        # Setup
        target = "; rm -rf test_file.txt"
        nm_command = "nm"
        max_depth = 10

        # Call the function with the malicious target
        GetSymbolTrie(target, nm_command, max_depth)

        self.assertFalse(os.path.exists('test_file.txt'))

if __name__ == '__main__':
    unittest.main()

