import unittest
import os
import distutils.spawn
import tempfile as _tempfile
import subprocess as _subprocess
import platform as _platform
from tensor231 import _run_deprecated_conversion_binary

class TestCommandInjection(unittest.TestCase):
    def test_run_deprecated_conversion_binary(self):

        # Define a dummy command to be injected
        injected_command = "; rm -rf /tmp/testfile"
        model_flags_str1="model_flags"
        conversion_flags_str1="conversion_flags"
        input_data_str1="input_data"

        # Create a test file that will be removed if command injection is successful
        with open("/tmp/testfile", "w") as f:
            f.write("This is a test file.")

        # Run the function with the injected command
        _run_deprecated_conversion_binary(
            model_flags_str=model_flags_str1.encode('utf-8'),
            conversion_flags_str=model_flags_str1.encode('utf-8'),
            input_data_str=model_flags_str1.encode('utf-8'),
            debug_info_str=injected_command.encode('utf-8')
        )

        # Check if the test file has been removed
        self.assertFalse(os.path.exists("/tmp/testfile"))

if __name__ == "__main__":
    unittest.main()

