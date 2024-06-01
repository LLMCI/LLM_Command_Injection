import unittest
import subprocess
import os
from typing import Dict, Tuple, Any

IS_WINDOWS = False

class TestCommandInjection(unittest.TestCase):
    def _popen(self, args: Tuple, env: Dict[str, str]) -> subprocess.Popen:
        kwargs: Dict[str, Any] = {}
        if not IS_WINDOWS:
            kwargs['start_new_session'] = True
        return subprocess.Popen(
            args=args,
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            **kwargs
        )

    def test_command_injection(self):
        # Create a test file
        with open('test_file.txt', 'w') as f:
            f.write('This is a test file')

        # Ensure the test file exists
        self.assertTrue(os.path.exists('test_file.txt'))

        # Attempt to delete the test file via command injection
        self._popen(('rm', 'test_file.txt'), {})

        # Check if the file was deleted
        self.assertFalse(os.path.exists('test_file.txt'))

if __name__ == '__main__':
    unittest.main()

