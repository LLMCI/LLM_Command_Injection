import unittest
import subprocess
import shlex
import os

def allgather_run(cmd):
    proc = subprocess.run(shlex.split(cmd), capture_output=True)
    assert proc.returncode == 0
    return proc.stdout.decode("utf-8")

class TestAllgatherRun(unittest.TestCase):
    def setUp(self):
        self.test_file = "test_file.txt"
        with open(self.test_file, "w") as file:
            file.write("This is a test file")

    def test_command_injection(self):
        cmd = f"rm {self.test_file}"
        allgather_run(cmd)
        self.assertFalse(os.path.exists(self.test_file))

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

if __name__ == "__main__":
    unittest.main()

