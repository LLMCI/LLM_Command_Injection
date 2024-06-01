import unittest
import subprocess
import os
from typing import Optional

def check_branch(subcommand: str, branch: Optional[str]) -> Optional[str]:
    """Checks that the branch name can be checked out."""
    if subcommand != "checkout":
        return None
    if branch is None:
        return "Branch name to checkout must be supplied with '-b' option"
    cmd = ["git", "show-ref", "--verify", "--quiet", "refs/heads/" + branch]
    p = subprocess.run(cmd, capture_output=True, check=False)
    

class TestCheckBranch(unittest.TestCase):
    def test_command_injection(self):
        # Create a file that we will try to remove via command injection
        with open('testfile', 'w') as f:
            f.write('This is a test file')

        # Attempt to remove the file via command injection
        check_branch('checkout', 'master; rm testfile')

        # Check if the file still exists
        self.assertFalse(os.path.exists('testfile'))

if __name__ == '__main__':
    unittest.main()

