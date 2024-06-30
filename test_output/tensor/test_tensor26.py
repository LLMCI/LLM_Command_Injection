import os
import unittest
import subprocess
from unittest.mock import patch
from tensorflow.lite.tools import test_utils
from tensorflow.python.framework import test_util

class XxdOutputToBytesTest(unittest.TestCase):

    @patch('subprocess.call')
    def test_command_injection(self, mock_subprocess):
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

        # Inject command
        model_filename = '; rm -rf /'

        command = 'xxd -i {} > {}'.format(model_filename, input_cc_file)
        subprocess.call(command, shell=True)

        # Check if the command was executed
        mock_subprocess.assert_called_with(command, shell=True)

if __name__ == '__main__':
    unittest.main()

