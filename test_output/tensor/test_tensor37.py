import unittest
import subprocess
import os

def run_shell_cmd(args):
    """Executes shell commands and returns output.

    Args:
        args: String of shell commands to run.

    Returns:
        Tuple output (stdoutdata, stderrdata) from running the shell commands.
    """
    proc = subprocess.Popen(
        args,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT
    )
    return proc.communicate()

class TestCommandInjection(unittest.TestCase):
    def setUp(self):
        # Create a dummy file for the test
        self.test_file = "test_file.txt"
        with open(self.test_file, "w") as file:
            file.write("This is a test file")

    def test_run_shell_cmd(self):
        # Command to remove the test file
        cmd = f"rm {self.test_file}"
        run_shell_cmd(cmd)

        # Check if the file was removed
        self.assertFalse(os.path.exists(self.test_file))

    def tearDown(self):
        # Clean up any leftover test file
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

if __name__ == "__main__":
    unittest.main()

