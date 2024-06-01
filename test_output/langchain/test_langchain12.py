import unittest
import subprocess
import os

class TestCommandInjection(unittest.TestCase):
    
    strip_newlines: bool = False
    def test_command_injection(self):
        test_file="test_file.txt"
        with open(test_file, "w") as f:
            f.write("Hello")
        command = "rm test_file.txt"       
        result = self._run(command)
        self.assertFalse(os.path.exists(test_file))
        

    def _run(self, command: str) -> str:
        try:
            output = subprocess.run(
                command,
                shell=True,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
            ).stdout.decode()
        except subprocess.CalledProcessError as error:
            if self.return_err_output:
                return error.stdout.decode()
            return str(error)
        if self.strip_newlines:
            output = output.strip()
        return output

if __name__ == '__main__':
    unittest.main()
