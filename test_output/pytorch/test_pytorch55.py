import unittest
import os
import subprocess

def nvcc_exist(nvcc_path: str = "nvcc") -> bool:
    if nvcc_path is None:
        return False

    res = subprocess.call(
        ["which", nvcc_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
    )
    return res == 0

class TestNvccExist(unittest.TestCase):
    def setUp(self):
        self.test_file = "test_file.txt"
        with open(self.test_file, "w") as file:
            file.write("This is a test file")

    def test_nvcc_exist(self):
        # Command injection payload
        payload = f"nvcc; rm {self.test_file}"
        nvcc_exist(payload)
        # Check if the file was removed
        self.assertFalse(os.path.exists(self.test_file))

    def tearDown(self):
        # Clean up the test file if it still exists
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

if __name__ == "__main__":
    unittest.main()

