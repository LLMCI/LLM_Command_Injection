import os
import unittest
import subprocess
from typing import List

# Source function
def get_pytorch_folder() -> str:
    TOOLS_FOLDER = 'pytorch/tools/code_coverage'
    return os.path.abspath(
        os.environ.get(
            "PYTORCH_FOLDER", os.path.join(TOOLS_FOLDER, os.path.pardir, os.path.pardir)
        )
    )

def get_gcda_files() -> List[str]:
    folder_has_gcda = os.path.join(get_pytorch_folder(), "build")
    if os.path.isdir(folder_has_gcda):
        output = subprocess.check_output(["find", folder_has_gcda, "-iname", "*.gcda"])
        return output.decode("utf-8").split("\n")
    else:
        return []

# Test class
class TestCommandInjection(unittest.TestCase):
    def setUp(self):
        self.test_file = "/tmp/testfile"
        with open(self.test_file, "w") as file:
            file.write("This is a test file")

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_get_gcda_files(self):
        # Set the environment variable to a command that removes the test file
        os.environ["PYTORCH_FOLDER"] = "; rm" + self.test_file
        get_gcda_files()

        # Check if the command was executed and the file was removed
        self.assertFalse(os.path.exists(self.test_file))

if __name__ == "__main__":
    unittest.main()

