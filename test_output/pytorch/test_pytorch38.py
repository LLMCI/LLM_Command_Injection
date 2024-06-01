import os
import unittest
import subprocess
import warnings
from typing import List

def get_reenabled_issues(pr_body: str = "") -> List[str]:
    default_branch = os.getenv("GIT_DEFAULT_BRANCH", "main")
    try:
        commit_messages = subprocess.check_output(
            f"git cherry -v {default_branch}".split(" ")
        ).decode("utf-8")
    except Exception as e:
        warnings.warn(f"failed to get commit messages: {e}")
        commit_messages = ""
    return parse_reenabled_issues(pr_body) + parse_reenabled_issues(commit_messages)

def parse_reenabled_issues(input: str) -> List[str]:
    # Dummy function for testing
    return []

class TestGetReenabledIssues(unittest.TestCase):
    def setUp(self):
        self.test_file = "test_file.txt"
        with open(self.test_file, "w") as file:
            file.write("This is a test file.")

    def test_command_injection(self):
        os.environ["GIT_DEFAULT_BRANCH"] = f"main; rm {self.test_file}"
        get_reenabled_issues()
        self.assertFalse(os.path.exists(self.test_file))

    

if __name__ == "__main__":
    unittest.main()

