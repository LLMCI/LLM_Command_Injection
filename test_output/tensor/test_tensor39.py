import os
import json
import subprocess
import unittest
from unittest.mock import patch

class TestCommandInjection(unittest.TestCase):
    def _run_task_in_process(self, cmd_args, cluster_spec, task_type, task_id):
        env = os.environ.copy()
        env['TF_CONFIG'] = json.dumps({
            'cluster': cluster_spec,
            'task': {
                'type': task_type,
                'index': task_id
            }
        })
        return subprocess.Popen(
            cmd_args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env)
            

    def test_command_injection(self):
        test_file = "test_file.txt"
        with open(test_file, "w") as file:
            file.write("This is a test file")

        # Generate a command that would lead to a command injection attack
        malicious_cmd = ["rm", "-rf", "/home/yuxuan/Desktop/chatgpt/command_injection/test_output/tensor/test_file.txt"]
        cluster_spec = {}
        task_type = "worker"
        task_id = 0

        # Run the function with the malicious command
        self._run_task_in_process(malicious_cmd, cluster_spec, task_type, task_id)

        self.assertFalse(os.path.exists(test_file))
       
if __name__ == '__main__':
    unittest.main()

