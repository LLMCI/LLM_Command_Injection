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
    if exitcode == 0:
      with gfile.Open(output_file, 'rb') as model_file:
        content = model_file.read()
      self.assertEqual(content is not None, should_succeed)
      if expected_ops_in_converted_model:
        op_set = tflite_test_util.get_ops_list(content)
        for opname in expected_ops_in_converted_model:
          self.assertIn(opname, op_set)
      if expected_output_shapes:
        output_shapes = tflite_test_util.get_output_shapes(content)
        self.assertEqual(output_shapes, expected_output_shapes)
      os.remove(output_file)
    else:
      self.assertFalse(should_succeed)
