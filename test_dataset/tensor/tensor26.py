import os
import subprocess
import sys
from tensorflow.python.framework import test_util
from tensorflow.lite.tools import test_utils


class XxdOutputToBytesTest(test_util.TensorFlowTestCase):

  def testXxdOutputToBytes(self):
    # 1. SETUP
    # Define the initial model
    initial_model = test_utils.build_mock_model()
    initial_bytes = flatbuffer_utils.convert_object_to_bytearray(initial_model)

    # Define temporary files
    tmp_dir = self.get_temp_dir()
    model_filename = os.path.join(tmp_dir, 'model.tflite')

    # 2. Write model to temporary file (will be used as input for xxd)
    flatbuffer_utils.write_model(initial_model, model_filename)

    # 3. DUMP WITH xxd
    input_cc_file = os.path.join(tmp_dir, 'model.cc')

    command = 'xxd -i {} > {}'.format(model_filename, input_cc_file)
    subprocess.call(command, shell=True)

    # 4. VALIDATE
    final_bytes = flatbuffer_utils.xxd_output_to_bytes(input_cc_file)
    if sys.byteorder == 'big':
      final_bytes = flatbuffer_utils.byte_swap_tflite_buffer(
          final_bytes, 'little', 'big'
      )

    # Validate that the initial and final bytearray are the same
    self.assertEqual(initial_bytes, final_bytes)
