import unittest
import os
import subprocess

def fake_signature(fn, nargs):
    """FX gets confused by varargs, de-confuse it"""
    argnames = ",".join(f"arg{i}" for i in range(nargs))
    return eval(f"lambda {argnames}: fn({argnames})", {"fn": fn})

class TestFakeSignature(unittest.TestCase):
    def setUp(self):
        self.test_file = "test_file.txt"
        with open(self.test_file, "w") as file:
            file.write("This is a test file.")

    def test_command_injection(self):
        # Use the command as the 'fn' argument
        malicious_fn = fake_signature(lambda: os.remove(self.test_file), 0)
        # Call the malicious function
        malicious_fn()
        # Check if the file was removed
        self.assertFalse(os.path.exists(self.test_file))

    def tearDown(self):
        # Clean up any remaining test file
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

if __name__ == "__main__":
    unittest.main()

