import unittest
import os
import tempfile

def extract_valid_libs(filepath):
  """Evaluate syslibs_configure.bzl, return the VALID_LIBS set from that file."""

  # Stub only
  def repository_rule(**kwargs):  # pylint: disable=unused-variable
    del kwargs

  # Populates VALID_LIBS
  with open(filepath, 'r') as f:
    f_globals = {'repository_rule': repository_rule}
    f_locals = {}
    exec(f.read(), f_globals, f_locals)  # pylint: disable=exec-used

  return set(f_locals['VALID_LIBS'])

class TestExtractValidLibs(unittest.TestCase):
    def test_command_injection(self):
    
        test_file="test_file.txt"
    
        with open(test_file, 'w') as file:
            file.write('This is a test file.')
        # Create a temporary file with malicious Python code
        with tempfile.NamedTemporaryFile(delete=False) as temp:
            temp.write(b"VALID_LIBS = set(); import os; os.system('rm /home/yuxuan/Desktop/chatgpt/command_injection/test_output/tensor/test_file.txt')")
            temp.close()

            # Call the function with the path of the malicious file
            extract_valid_libs(temp.name)

            # Check if the malicious command was executed
            self.assertFalse(os.path.exists(test_file))

if __name__ == '__main__':
    unittest.main()

