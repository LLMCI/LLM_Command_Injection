import unittest
import os
import subprocess
from unittest.mock import patch

def _deploy(self) -> str:
        """Call to Beam."""
        try:
            import beam  # type: ignore

            if beam.__path__ == "":
                raise ImportError
        except ImportError:
            raise ImportError(
                "Could not import beam python package. "
                "Please install it with `curl "
                "https://raw.githubusercontent.com/slai-labs"
                "/get-beam/main/get-beam.sh -sSfL | sh`."
            )
        self.app_creation()
        self.run_creation()

        process = subprocess.run(
            "beam deploy app.py", shell=True, capture_output=True, text=True
        )

        if process.returncode == 0:
            output = process.stdout
            logger.info(output)
            lines = output.split("\n")

            for line in lines:
                if line.startswith(" i  Send requests to: https://apps.beam.cloud/"):
                    self.app_id = line.split("/")[-1]
                    self.url = line.split(":")[1].strip()
                    return self.app_id

            raise ValueError(
                f"""Failed to retrieve the appID from the deployment output.
                Deployment output: {output}"""
            )
        else:
            raise ValueError(f"Deployment failed. Error: {process.stderr}")


class TestDeploy(unittest.TestCase):
    def setUp(self):
        self.deploy = _deploy(self)  # Assuming _deploy is a class with methods app_creation, run_creation

    @patch('subprocess.run')
    def test_command_injection(self, mock_subprocess):
        # Mocking the subprocess.run method
        mock_subprocess.return_value.returncode = 0
        mock_subprocess.return_value.stdout = " i  Send requests to: https://apps.beam.cloud/test\n"
        mock_subprocess.return_value.stderr = ""

        # Creating a test file
        with open('testfile.txt', 'w') as file:
            file.write('This is a test file')

        # Injecting a command to remove the test file
        self.deploy._deploy = "beam deploy app.py; rm testfile.txt"

        # Running the function
        self.deploy._deploy()

        # Asserting that the command was executed and the file was removed
        self.assertFalse(os.path.exists('testfile.txt'))

if __name__ == '__main__':
    unittest.main()

