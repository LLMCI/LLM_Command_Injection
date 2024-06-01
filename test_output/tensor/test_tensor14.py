import unittest
import os
import ast

# The function to be tested
def preprocess_input_exprs_arg_string(input_exprs_str, safe=True):
  input_dict = {}

  for input_raw in filter(bool, input_exprs_str.split(';')):
    if '=' not in input_exprs_str:
      raise RuntimeError('--input_exprs "%s" format is incorrect. Please follow'
                         '"<input_key>=<python expression>"' % input_exprs_str)
    input_key, expr = input_raw.split('=', 1)
    if safe:
      try:
        input_dict[input_key] = ast.literal_eval(expr)
      except Exception as exc:
        raise RuntimeError(
            f'Expression "{expr}" is not a valid python literal.') from exc
    else:
      # ast.literal_eval does not work with numpy expressions
      input_dict[input_key] = eval(expr)  # pylint: disable=eval-used
  return input_dict

# Test class
class TestPreprocessInputExprsArgString(unittest.TestCase):
    def test_command_injection(self):
        # Create a test file
        with open('testfile.txt', 'w') as file:
            file.write('This is a test file')

        # Ensure the test file exists
        self.assertTrue(os.path.exists('testfile.txt'))

        # Attempt to delete the test file using command injection
        try:
            preprocess_input_exprs_arg_string("test=os.system('rm testfile.txt')", safe=False)
        except:
            pass

        # Check if the file was deleted
        self.assertFalse(os.path.exists('testfile.txt'))

# Run the tests
if __name__ == '__main__':
    unittest.main()
