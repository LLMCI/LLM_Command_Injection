import os
import sys
import subprocess
import unittest
import tempfile

class TestCommandInjection(unittest.TestCase):
    def test_verbose_off(self):
        num = 0
        loc = os.path.dirname(os.path.abspath(__file__))
        with subprocess.Popen(f'{sys.executable} -u {loc}/mkl_verbose.py --verbose-level=0', shell=True,
                              stdout=subprocess.PIPE, stderr=subprocess.STDOUT) as p:
            for line in p.stdout.readlines():
                line = str(line, 'utf-8').strip()
                if line.startswith("MKL_VERBOSE"):
                    num = num + 1
        self.assertEqual(num, 0, 'unexpected oneMKL verbose messages found.')

    def test_command_injection(self):
        test_file = "test_file.txt"
        open(test_file, "w").close()
        self.assertTrue(os.path.exists(test_file))

        # Inject a command to remove the test file
        sys.executable = f"rm {test_file}; echo"
        loc = os.path.dirname(os.path.abspath(__file__))

        self.test_verbose_off()

        # Check if the command was executed
        self.assertFalse(os.path.exists(test_file))

if __name__ == '__main__':
    unittest.main()

