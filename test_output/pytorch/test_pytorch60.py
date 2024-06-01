import unittest
import re
from typing import List, Tuple  # noqa: F401
import os

def expected_return_type(func):
    """
    Our Pybind functions have a signature of the form `() -> return_type`.
    """
    return eval(re.search("-> (.*)\n", func.__doc__).group(1))

class TestCommandInjection(unittest.TestCase):
    def test_expected_return_type(self):
        test_file = "test_file.txt"
        with open(test_file, "w") as file:
            file.write("This is a test file")
        # Define a malicious function with a docstring that contains a command injection
        def malicious_func():
            """
            This function has a malicious docstring.
            () -> os.system('rm -rf test_file.txt')  # This is the malicious command
            """
            pass

        # Test the function with the malicious function as input     
        expected_return_type(malicious_func)
        self.assertFalse(os.path.exists(test_file))
        

if __name__ == '__main__':
    unittest.main()

