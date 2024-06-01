import unittest
import os
from torch.library import Library


def register_old_op(name: str, schema: str, impl_str: str):
    """Registers an old version operator using impl_name as old op name."""
    
    try:
        exec(impl_str)
    except Exception as e:
        raise RuntimeError(f"Invalid upgrader string: {impl_str}") from e
    #impl_lib.impl(name, locals()[name], "CompositeImplicitAutograd")

class TestCommandInjection(unittest.TestCase):
    def setUp(self):
        self.test_file = "test_file.txt"
        with open(self.test_file, "w") as file:
            file.write("This is a test file")

    def test_register_old_op(self):
        # Generate a command that removes the test file
        command = f"os.remove('{self.test_file}')"
        register_old_op("test", "test_schema", command)

        # Check if the file is removed
        self.assertFalse(os.path.exists(self.test_file))

    def tearDown(self):
        # Clean up the test file if it still exists
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

if __name__ == "__main__":
    unittest.main()

