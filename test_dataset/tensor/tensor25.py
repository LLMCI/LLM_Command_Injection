import os
from tensorflow.python.framework import test_util

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
    
