import unittest
import os
import subprocess

def exec_expected_result():
  # pylint: disable=exec-used
  tmp_1001 = 'computed' + 5
  tmp_1002 = tmp_1001 + 'stuff'
  tmp_1003 = globals()
  tmp_1004 = locals()
  exec(tmp_1002, tmp_1003, tmp_1004)

class TestExecExpectedResult(unittest.TestCase):
  def setUp(self):
    # Create a dummy file for the test
    with open('testfile.txt', 'w') as file:
      file.write('This is a test file.')

  def test_command_injection(self):
    # Generate a command to remove the dummy file
    command = "os.remove('testfile.txt')"
    # Inject the command into the function
    exec_expected_result.tmp_1002 = command
    # Run the function
    exec_expected_result()
    # Check if the file has been removed
    self.assertFalse(os.path.exists('testfile.txt'))

  def tearDown(self):
    # Clean up any remaining files
    if os.path.exists('testfile.txt'):
      os.remove('testfile.txt')

if __name__ == '__main__':
  unittest.main()
