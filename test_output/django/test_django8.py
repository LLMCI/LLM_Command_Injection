import unittest
import os
import subprocess
import shutil
from unittest.mock import patch, MagicMock

def run_formatters(written_files, black_path=(sentinel := object())):
    """
    Run the black formatter on the specified files.
    """
    # Use a sentinel rather than None, as which() returns None when not found.
    if black_path is sentinel:
        black_path = shutil.which("black")
    if black_path:
        subprocess.run(
            [black_path, "--fast", "--", *written_files],
            capture_output=True,
        )

class TestRunFormatters(unittest.TestCase):
    @patch('subprocess.run')
    def test_run_formatters_injection(self, mock_run):
        # Create a test file
        with open('test_file', 'w') as f:
            f.write('test')

        # Run the function with a command injection payload
        run_formatters('rm test_file', '/home/yuxuan/Desktop/chatgpt/command_injection/test_output/django/black')

        # Check if the command injection payload was executed
        self.assertFalse(os.path.exists('test_file'))

        # Clean up
        if os.path.exists('test_file'):
            os.remove('test_file')

if __name__ == '__main__':
    unittest.main()

