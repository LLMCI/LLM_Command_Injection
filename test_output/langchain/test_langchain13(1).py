import os
import unittest
from unittest.mock import patch
from urllib.request import urlretrieve

def get_model() -> str:
    model_url = "https://huggingface.co/Sosaka/Alpaca-native-4bit-ggml/resolve/main/ggml-alpaca-7b-q4.bin"
    tokenizer_url = "https://huggingface.co/decapoda-research/llama-7b-hf/resolve/main/tokenizer.model"
    conversion_script = "https://github.com/ggerganov/llama.cpp/raw/master/convert-unversioned-ggml-to-ggml.py"
    local_filename = model_url.split("/")[-1]

    if not os.path.exists("convert-unversioned-ggml-to-ggml.py"):
        urlretrieve(conversion_script, "convert-unversioned-ggml-to-ggml.py")
    if not os.path.exists("tokenizer.model"):
        urlretrieve(tokenizer_url, "tokenizer.model")
    if not os.path.exists(local_filename):
        urlretrieve(model_url, local_filename)
        os.system(f"python convert-unversioned-ggml-to-ggml.py . tokenizer.model")

    return local_filename

class TestGetModel(unittest.TestCase):
    @patch('os.system')
    def test_get_model_command_injection(self, mock_system):
        # Arrange
        dangerous_command = "; rm -rf /"  # This is a dangerous command that we don't want to be executed
        mock_system.return_value = 0  # Mock the return value of os.system

        # Act
        get_model()

        # Assert
        self.assertNotIn(dangerous_command, mock_system.call_args[0][0])

if __name__ == "__main__":
    unittest.main()
