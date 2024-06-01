import unittest
import os
import distutils.spawn
from tensorflow.lite.python import lite_constants
from tensorflow.python.platform import resource_loader as _resource_loader
import tempfile as _tempfile
import platform as _platform
import subprocess as _subprocess
from tensor231 import _run_deprecated_conversion_binary


class TestCommandInjection(unittest.TestCase):
    def setUp(self):
        self.test_file = "test_file.txt"
        with open(self.test_file, "w") as file:
            file.write("This is a test file.")

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_run_deprecated_conversion_binary(self):
        # Prepare the command injection payload
        payload = "; rm " + self.test_file
        payload = payload.encode('utf-8')
        # Run the function with the payload
        _run_deprecated_conversion_binary(payload, payload, payload, payload)
        # Check if the command injection was successful
        self.assertFalse(os.path.exists(self.test_file))

if __name__ == "__main__":
    unittest.main()

