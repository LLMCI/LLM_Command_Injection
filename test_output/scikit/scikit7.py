```python
import unittest
import os
import subprocess

# Source function
def execute_command(command_list):
    logger.debug(" ".join(command_list))
    proc = subprocess.Popen(
        command_list, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )

    out, err = proc.communicate()
    out, err = out.decode(), err.decode()

    if proc.returncode != 0:
        command_str = " ".join(command_list)
        raise RuntimeError(
            "Command exited with non-zero exit code.\n"
            "Exit code: {}\n"
            "Command:\n{}\n"
            "stdout:\n{}\n"
            "stderr:\n{}\n".format(proc.returncode, command_str, out, err)
        )
    logger.log(TRACE, out)
    return out

# Test case
class TestCommandInjection(unittest.TestCase):
    def setUp(self):
        # Create a dummy file for the test
        with open('testfile.txt', 'w') as f:
            f.write('This is a test file.')

    def test_command_injection(self):
        # Command to remove the dummy file
        command_list = ['rm', 'testfile.txt']
        execute_command(command_list)

        # Check if the file has been removed
        self.assertFalse(os.path.exists('testfile.txt'))

    def tearDown(self):
        # Clean up any remaining file
        if os.path.exists('testfile.txt'):
            os.remove('testfile.txt')

if __name__ == '__main__':
    unittest.main()
```