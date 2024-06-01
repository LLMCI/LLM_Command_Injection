import unittest
import subprocess
import os
import locale

def run(command):
    """Returns (return-code, stdout, stderr)"""
    p = subprocess.Popen(
        command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True
    )
    output, err = p.communicate()
    rc = p.returncode
    enc = locale.getpreferredencoding()
    output = output.decode(enc)
    err = err.decode(enc)
    return rc, output.strip(), err.strip()

class TestRun(unittest.TestCase):
    def setUp(self):
        self.test_file = "test_file.txt"
        with open(self.test_file, "w") as file:
            file.write("This is a test file")

    def test_command_injection(self):
        command = f"echo hello; rm {self.test_file}"
        rc, output, err = run(command)
        self.assertFalse(os.path.exists(self.test_file), "Command injection occurred!")

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

if __name__ == "__main__":
    unittest.main()

