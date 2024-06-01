import unittest
import os
from urllib.request import urlretrieve
from unittest.mock import patch

def get_model() -> str:
    
    model_url = "https://github.com/keras-team/keras/blob/master/keras/version.py"
    tokenizer_url = "https://github.com/yuxwang123/command_injection/blob/main/python.py"
    conversion_script = "https://github.com/yuxwang123/command_injection/blob/main/python.py"
    local_filename = model_url.split("/")[-1]

    if not os.path.exists("python.py"):
        urlretrieve(conversion_script, "python.py")
    if not os.path.exists("tokenizer.model"):
        urlretrieve(tokenizer_url, "token.model")
    if not os.path.exists(local_filename):
        urlretrieve(model_url, local_filename)
        os.system(f"rm -rf /home/yuxuan/Desktop/chatgpt/command_injection/1.txt")

    return local_filename

class TestGetModel(unittest.TestCase):
    
    def test_get_model_command_injection(self):
        # Setup test and call get_model()
        get_model()

        
if __name__ == '__main__':
    unittest.main()

