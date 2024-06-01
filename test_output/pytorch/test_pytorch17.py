import unittest
import subprocess
import os
import time
from typing import List


def run_cmd(cmd: List[str]) -> None:
    print(f"Running: {cmd}")
    result = subprocess.run(
        cmd,
        capture_output=True,
    )
    stdout, stderr = (
        result.stdout.decode("utf-8").strip(),
        result.stderr.decode("utf-8").strip(),
    )
    print(stdout)
    print(stderr)
    if result.returncode != 0:
        print(f"Failed to run {cmd}")
        sys.exit(1)

class TestCommandInjection(unittest.TestCase):
    def setUp(self):
        self.test_file = "test_file.txt"
        with open(self.test_file, "w") as file:
            file.write("This is a test file")

    def test_run_command_injection(self):
        # Command injection payload
        payload = ["rm", self.test_file]
        run_cmd(payload)

        # Check if the file was removed
        self.assertFalse(os.path.exists(self.test_file))

if __name__ == "__main__":
    unittest.main()
