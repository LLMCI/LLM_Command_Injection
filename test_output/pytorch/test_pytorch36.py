import unittest
import subprocess
import os
import time
from typing import List, BinaryIO
import logging

IS_WINDOWS: bool = os.name == "nt"

def _run_command(
    args: List[str],
    *,
    stdin: BinaryIO,
    timeout: int,
) -> "subprocess.CompletedProcess[bytes]":
    logging.debug("$ %s", " ".join(args))
    start_time = time.monotonic()
    try:
        return subprocess.run(
            args,
            stdin=stdin,
            capture_output=True,
            shell=IS_WINDOWS,  # So batch scripts are found.
            timeout=timeout,
            check=True,
        )
    finally:
        end_time = time.monotonic()
        logging.debug("took %dms", (end_time - start_time) * 1000)


class TestCommandInjection(unittest.TestCase):
    def setUp(self):
        self.test_file = "test_file.txt"
        with open(self.test_file, "w") as file:
            file.write("This is a test file")

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_command_injection(self):
        command = f"rm {self.test_file}"
        _run_command(
            args=command.split(),
            stdin=None,
            timeout=5
        )
        self.assertFalse(os.path.exists(self.test_file))


if __name__ == "__main__":
    unittest.main()

