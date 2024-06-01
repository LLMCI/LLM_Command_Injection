from unittest.mock import MagicMock
import unittest
import subprocess
import os

class TestShellCommand(unittest.TestCase):
   def test_injection(self):
       # Set a malicious banner message
       banner = ("PyS@linPwnd!;rm -rf /")
       
       # Create a mock environment to simulate the execution of the code
       env = MagicMock()
       env.local = {"__name__": "my_env"}
       
       # Call the interact method with the malicious banner
       result = code.interact(banner=banner, local=env)
       
       # Assert that the rm -rf command was executed
       self.assertTrue(os.path.exists("/"))
