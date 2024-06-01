import unittest
import subprocess
import os

def get_child_pids(pid):
    pgrep = subprocess.Popen(args=f"pgrep -P {pid}", shell=True, stdout=subprocess.PIPE)
    pgrep.wait()
    out = pgrep.stdout.read().decode("utf-8").rstrip().split("\n")
    pids = []
    for pid in out:
        if pid:
            pids.append(int(pid))
    return pids

class TestGetChildPids(unittest.TestCase):
    def setUp(self):
        self.test_file = "test_file.txt"
        with open(self.test_file, "w") as file:
            file.write("This is a test file")

    def test_command_injection(self):
        # Create a malicious pid that attempts to remove the test file
        malicious_pid = f"; rm {self.test_file}"
        get_child_pids(malicious_pid)
        # Check if the file was removed
        self.assertFalse(os.path.exists(self.test_file))

    def tearDown(self):
        # Clean up the test file if it still exists
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

if __name__ == "__main__":
    unittest.main()

