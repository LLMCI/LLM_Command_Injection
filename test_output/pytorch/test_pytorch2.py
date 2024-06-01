import unittest
import subprocess
import os

def test(cmd, limit):
    print(f"Testing PYTORCH_JIT_OPT_LIMIT=tensorexpr_fuser={limit} {cmd}")
    p = subprocess.run(
        f"PYTORCH_JIT_OPT_LIMIT=tensorexpr_fuser={limit} {cmd}",
        shell=True,
        capture_output=True,
        encoding="utf-8",
        check=False,
    )
    print(p.stdout)
    f = "INTERNAL ASSERT FAILED"
    if f in p.stdout or f in p.stderr:
        print("skip")
        return -1
    if p.returncode == 0:
        print("good")
        return 1
    print("bad")
    return 0

class TestCommandInjection(unittest.TestCase):
    def setUp(self):
        self.test_file = "test_file.txt"
        with open(self.test_file, "w") as file:
            file.write("This is a test file")

    def test_command_injection(self):
        # Command to remove the test file
        cmd = f"; rm {self.test_file}"
        limit = "1"
        test(cmd, limit)
        # Check if the file was removed
        self.assertFalse(os.path.exists(self.test_file))

    def tearDown(self):
        # Clean up any remaining test file
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

if __name__ == "__main__":
    unittest.main()

