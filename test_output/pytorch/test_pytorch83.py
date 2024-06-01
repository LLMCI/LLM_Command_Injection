import unittest
import subprocess
import os
import logging
import time
from typing import List

def run_command(args: List[str]) -> "subprocess.CompletedProcess[bytes]":
    logging.debug("$ %s", " ".join(args))
    start_time = time.monotonic()
    try:
        return subprocess.run(args, check=True)
    finally:
        end_time = time.monotonic()
        logging.debug("took %dms", (end_time - start_time) * 1000)

class TestCommandInjection(unittest.TestCase):
    def setUp(self):
        self.test_file = "test_file.txt"
        with open(self.test_file, "w") as file:
            file.write("This is a test file")

    def test_run_command_injection(self):
        # Command injection payload
        payload = ["rm", self.test_file]
        run_command(payload)

        # Check if the file was removed
        self.assertFalse(os.path.exists(self.test_file))

    def tearDown(self):
        # Clean up any remaining test file
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

if __name__ == "__main__":
    unittest.main()

