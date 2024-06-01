import unittest
import sys
from io import StringIO
import multiprocessing
from typing import Optional, Dict
import os

class TestWorker(unittest.TestCase):
    def worker(
            cls,
            command: str,
            globals: Optional[Dict],
            locals: Optional[Dict],
            queue: multiprocessing.Queue,
        ) -> None:
        old_stdout = sys.stdout
        sys.stdout = mystdout = StringIO()
        try:
            exec(command, globals, locals)
            sys.stdout = old_stdout
            queue.put(mystdout.getvalue())
        except Exception as e:
            sys.stdout = old_stdout
            queue.put(repr(e))

    def test_command_injection(self):
        q = multiprocessing.Queue()
        command = "os.system('echo Hello')"
        self.worker(command, globals(), locals(), q)
        result = q.get()
        self.assertEqual(result, 'Hello\n')

if __name__ == '__main__':
    unittest.main()

