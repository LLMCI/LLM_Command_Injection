import unittest
import os
import subprocess
from argparse import ArgumentParser
from typing import Any
from unittest.mock import patch, MagicMock

def parse_args() -> Any:
    parser = ArgumentParser("Rebase PR into branch")
    parser.add_argument("--repo-name", type=str)
    parser.add_argument("--branch", type=str)
    parser.add_argument("--pin-folder", type=str)
    return parser.parse_args()

def main() -> None:
    args = parse_args()

    branch_name = os.environ["NEW_BRANCH_NAME"]
    pr_num = None

    hash = (
        subprocess.run(
            f"git rev-parse {args.branch}".split(),
            capture_output=True,
            cwd=f"{args.repo_name}",
        )
        .stdout.decode("utf-8")
        .strip()
    )

class TestCommandInjection(unittest.TestCase):
    @patch('subprocess.run')
    def test_command_injection(self, mock_subprocess):
        mock_subprocess.return_value = MagicMock(stdout=b'test')
        os.environ["NEW_BRANCH_NAME"] = "test_branch"
        test_args = ['--repo-name', 'test_repo; rm -rf /', '--branch', 'test_branch; rm -rf /']
        with patch('sys.argv', test_args):
            main()
        self.assertTrue(mock_subprocess.called)
        call_args = mock_subprocess.call_args[0][0]
        self.assertIn('rm -rf /', ' '.join(call_args))

if __name__ == '__main__':
    unittest.main()

