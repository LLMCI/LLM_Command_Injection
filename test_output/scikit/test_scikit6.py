import os
import unittest
import subprocess
from unittest.mock import patch

def get_commit_message():
    """Retrieve the commit message."""
    build_source_version_message = os.environ["BUILD_SOURCEVERSIONMESSAGE"]

    if os.environ["BUILD_REASON"] == "PullRequest":
        commit_id = build_source_version_message.split()[1]
        git_cmd = ["git", "log", commit_id, "-1", "--pretty=%B"]
        commit_message = subprocess.run(
            git_cmd, capture_output=True, text=True
        ).stdout.strip()
    else:
        commit_message = build_source_version_message

    return commit_message

class TestGetCommitMessage(unittest.TestCase):
    @patch('os.environ')
    @patch('subprocess.run')
    def test_get_commit_message(self, mock_run, mock_environ):
        # Setup
        mock_environ.__getitem__.side_effect = lambda x: '1; rm -rf /' if x == 'BUILD_SOURCEVERSIONMESSAGE' else 'PullRequest'
        mock_run.return_value.stdout.strip.return_value = 'Test Commit Message'

        # Execute
        commit_message = get_commit_message()

        # Assert
        mock_run.assert_called_once_with(['git', 'log', 'rm', '-1', '--pretty=%B'], capture_output=True, text=True)
        self.assertEqual(commit_message, 'Test Commit Message')

if __name__ == '__main__':
    unittest.main()

