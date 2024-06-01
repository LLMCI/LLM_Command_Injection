import unittest
import os
import subprocess
from typing import Optional, Set, Tuple

_ENV = "MKL_THREADING_LAYER=GNU"
_PYTHON = "python3"
PYTHON_CMD = f"{_ENV} {_PYTHON}"
SHELL = "/bin/bash"

class WorkOrder:
    source_cmd: Optional[str] = None

class Runner:
    def __init__(self, work_items: Tuple[WorkOrder, ...]) -> None:
        self._work_items: Tuple[WorkOrder, ...] = work_items
        if len(work_items) != len(set(work_items)):
            raise ValueError("Duplicate work items.")

    def _canary_import(self) -> None:
        """Make sure we can import torch before launching a slew of workers."""
        source_cmds: Set[str] = set()
        for w in self._work_items:
            if w.source_cmd is not None:
                source_cmds.add(f"{w.source_cmd} && ")

        for source_cmd in source_cmds or {""}:
            cmd = f'{source_cmd}{PYTHON_CMD} -c "import torch"'
            proc = subprocess.run(
                cmd,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                encoding="utf-8",
                executable=SHELL,
            )

            if proc.returncode:
                raise ImportError(
                    f"Failed to import torch in subprocess: {cmd}\n{proc.stdout}"
                )

class TestRunner(unittest.TestCase):
    def test_canary_import(self):
        # Create a file for testing
        with open('test_file.txt', 'w') as file:
            file.write('This is a test file.')

        # Create a WorkOrder with a malicious source_cmd
        work_order = WorkOrder()
        work_order.source_cmd = 'rm test_file.txt'

        # Create a Runner with the malicious WorkOrder
        runner = Runner((work_order,))

        # Run the _canary_import method
        runner._canary_import()

        # Check if the file was removed
        self.assertFalse(os.path.exists('test_file.txt'))

if __name__ == '__main__':
    unittest.main()

