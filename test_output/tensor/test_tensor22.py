import unittest
import os
import sys
import subprocess

def _if_spawn_run_and_exit():
  is_spawned = ('-c' in sys.argv[1:] and
                sys.argv[sys.argv.index('-c') +
                         1].startswith('from multiprocessing.'))

  if not is_spawned:
    return
  cmd = sys.argv[sys.argv.index('-c') + 1]
  sys.argv = sys.argv[0:1]

  exec(cmd)
  sys.exit(0)

class TestCommandInjection(unittest.TestCase):
    def setUp(self):
        self.test_file = "test_file.txt"
        with open(self.test_file, "w") as file:
            file.write("This is a test file")

    def test_command_injection(self):
        # Generate an os command to remove a file
        command = f"from multiprocessing.spawn import spawn_main; import os; os.remove('{self.test_file}')"
        sys.argv = ['test_script.py', '-c', command]

        # Run the function
        with self.assertRaises(SystemExit):
            _if_spawn_run_and_exit()

        # Check if the command is executed by verifying if the file is removed
        self.assertFalse(os.path.exists(self.test_file))

    def tearDown(self):
        # Clean up the test file if it still exists
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

if __name__ == "__main__":
    unittest.main()
