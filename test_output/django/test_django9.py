import os
import unittest
from unittest.mock import patch, mock_open
from django.core.management import BaseCommand
from django9 import Command

class CommandInjectionTest(unittest.TestCase):
    def setUp(self):
        self.command = Command(BaseCommand)

    @patch('os.path.isfile', return_value=True)
    @patch('os.environ.get', return_value='PYTHONSTARTUP')
    @patch('builtins.open', new_callable=mock_open, read_data='__import__("os").system("rm -rf text_file")')    
    def test_python_command_injection(self, mock_file, mock_env, mock_isfile):
        with self.assertRaises(OSError):
            self.command.python({"no_startup": False})
    
if __name__ == '__main__':
    unittest.main()

