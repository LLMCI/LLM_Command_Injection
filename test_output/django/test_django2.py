import unittest
import os
import subprocess
import datetime
from unittest.mock import patch

def get_git_changeset():
    if "__file__" not in globals():
        return None
    repo_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    git_log = subprocess.run(
        "git log --pretty=format:%ct --quiet -1 HEAD",
        capture_output=True,
        shell=True,
        cwd=repo_dir,
        text=True,
    )
    timestamp = git_log.stdout
    tz = datetime.timezone.utc
    try:
        timestamp = datetime.datetime.fromtimestamp(int(timestamp), tz=tz)
    except ValueError:
        return None
    return timestamp.strftime("%Y%m%d%H%M%S")

class TestGetGitChangeset(unittest.TestCase):
    @patch('subprocess.run')
    def test_get_git_changeset_injection(self, mock_subprocess):
        # Arrange
        mock_subprocess.return_value.stdout = 'rm -rf /'  # Dangerous command

        # Act
        result = get_git_changeset()

        # Assert
        mock_subprocess.assert_called_with(
            "git log --pretty=format:%ct --quiet -1 HEAD",
            capture_output=True,
            shell=True,
            cwd=os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            text=True,
        )
        self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()

