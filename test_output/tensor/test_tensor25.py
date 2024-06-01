import os
import unittest
from unittest.mock import patch
from tensorflow.python.framework import test_util
from tensorflow.python.platform import resource_loader

class TestModels(test_util.TensorFlowTestCase):

  def _run(self,
           flags_str,
           should_succeed,
           expected_ops_in_converted_model=None,
           expected_output_shapes=None):
    output_file = os.path.join(self.get_temp_dir(), 'model.tflite')
    tflite_bin = resource_loader.get_path_to_datafile('tflite_convert')
    cmdline = '{0} --output_file={1} {2}'.format(tflite_bin, output_file,
                                                 flags_str)

    exitcode = os.system(cmdline)
    

class TestCommandInjection(unittest.TestCase):

  
  def test_command_injection(self):
    test_model = TestModels()
    test_file="test_file.txt"
    
    with open(test_file, 'w') as file:
            file.write('This is a test file.')
    
    malicious_str = '; rm -rf test_file.txt'
    test_model._run(malicious_str, False)
    self.assertFalse(os.path.exists(test_file))
   

if __name__ == '__main__':
  unittest.main()

