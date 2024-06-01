import unittest
from argparse import ArgumentParser
import os
import subprocess

# The function to be tested
def update_catalogs(resources, languages):
    print("Updating catalogs...")

def lang_stats(resources, languages):
    print("Generating language statistics...")

def fetch(resources, languages):
    print("Fetching resources...")

RUNABLE_SCRIPTS = ("update_catalogs", "lang_stats", "fetch")

def run_script(cmd, resources=None, languages=None):
    parser = ArgumentParser()
    parser.add_argument("cmd", nargs=1, choices=RUNABLE_SCRIPTS)
    parser.add_argument(
        "-r",
        "--resources",
        action="append",
        help="limit operation to the specified resources",
    )
    parser.add_argument(
        "-l",
        "--languages",
        action="append",
        help="limit operation to the specified languages",
    )
    options = parser.parse_args([cmd] + (resources or []) + (languages or []))

    eval(options.cmd[0])(options.resources, options.languages)

# The test case
class TestCommandInjection(unittest.TestCase):
    def test_command_injection(self):
        # Create a file that should not be removed
        with open('testfile', 'w') as f:
            f.write('This is a test file.')

        # Try to inject a command to remove the file
        try:
            run_script('update_catalogs; os.remove("testfile")')
        except SystemExit:
            pass

        # Check if the file still exists
        self.assertTrue(os.path.exists('testfile'))

        # Clean up
        os.remove('testfile')

if __name__ == '__main__':
    unittest.main()

