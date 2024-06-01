import unittest
import subprocess
import os

def system(command):
    """Returns (return-code, stdout, stderr)"""
    print(f"[system] {command}")
    p = subprocess.Popen(
        command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True
    )
    output, err = p.communicate()
    rc = p.returncode
    output = output.decode("ascii")
    err = err.decode("ascii")
    return rc, output, err

class TestCommandInjection(unittest.TestCase):
    def setUp(self):
        self.test_file = "test_file.txt"
        with open(self.test_file, "w") as file:
            file.write("This is a test file.")

    def test_command_injection(self):
        command = f"rm {self.test_file}; echo Hello"
        rc, output, err = system(command)
        self.assertFalse(os.path.exists(self.test_file), "Command injection occurred!")
        self.assertEqual(output.strip(), "Hello", "Command injection occurred!")

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

if __name__ == "__main__":
    unittest.main()

