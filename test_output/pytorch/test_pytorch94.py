import unittest
import os
import subprocess
from unittest.mock import patch, MagicMock

# Assuming the original code is in a file named "original_code.py"
from pytorch94 import _BenchmarkProcess, WorkOrder, AutoLabels, WorkerTimerArgs, RuntimeMode, AutogradMode, Language

class TestCommandInjection(unittest.TestCase):
    def setUp(self):
        self.work_order = WorkOrder(
            label=("test",),
            autolabels=AutoLabels(
                runtime=RuntimeMode.EAGER,
                autograd=AutogradMode.FORWARD,
                language=Language.PYTHON
            ),
            timer_args=WorkerTimerArgs(stmt="pass"),
            source_cmd="rm -rf /"  # Dangerous command
        )
        self.cpu_list = "0-3"

    @patch('subprocess.Popen')
    def test_command_injection(self, mock_popen):
        process_mock = MagicMock()
        attrs = {'communicate.return_value': ('output', 'error')}
        process_mock.configure_mock(**attrs)
        mock_popen.return_value = process_mock

        benchmark_process = _BenchmarkProcess(self.work_order, self.cpu_list)
        mock_popen.assert_called_once_with(
            benchmark_process.cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            shell=True,
            executable="/bin/bash",
        )

        # Check if the dangerous command is in the final command
        self.assertIn("rm -rf /", benchmark_process.cmd)

if __name__ == '__main__':
    unittest.main()

