import unittest
import os
import sys
from datetime import datetime
from django.utils import timezone

class TestCommandInjection(unittest.TestCase):
    
    def _ask_default(self, default=""):
            code = input()
            if not code and default:
                code = default
            elif code == "exit":
                sys.exit(1)
            else:
                try:
                    return eval(code, {}, {"datetime": datetime, "timezone": timezone})
                except (SyntaxError, NameError) as e:
                    return 0

    def test_command_injection(self):
        test_file = "test_file.txt"
        open(test_file, "w").close()
        self.assertTrue(os.path.exists(test_file))
        self._ask_default(default="")
        self.assertFalse(os.path.exists(test_file))

if __name__ == '__main__':
    unittest.main()

