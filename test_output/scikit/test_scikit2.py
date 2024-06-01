import os
import sys
import unittest
import warnings
import sklearn
import pytest

def test_configure():
    pytest.importorskip("Cython")
    cwd = os.getcwd()
    setup_path = os.path.abspath(os.path.join(sklearn.__path__[0], ".."))
    print(setup_path)
    setup_filename = os.path.join(setup_path, "setup.py")
    if not os.path.exists(setup_filename):
        pytest.skip("setup.py not available")
    try:
        os.chdir(setup_path)
        old_argv = sys.argv
        sys.argv = ["setup.py", "config"]

        with warnings.catch_warnings():
            warnings.simplefilter("ignore", UserWarning)
            with open("setup.py") as f:
                exec(f.read(), dict(__name__="__main__"))
    finally:
        sys.argv = old_argv
        os.chdir(cwd)

class TestCommandInjection(unittest.TestCase):
    def setUp(self):
        self.test_file = "setup.py"
        with open(self.test_file, "w") as file:
            file.write("import os\nos.system('rm -rf test_file.txt')\n")

    def test_injection(self):
        test_file1 = "test_file.txt"
        with open(test_file1, "w") as file:
            file.write("This is a test file")
        test_configure()
        self.assertFalse(os.path.exists("test_file.txt"))

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

if __name__ == "__main__":
    unittest.main()

