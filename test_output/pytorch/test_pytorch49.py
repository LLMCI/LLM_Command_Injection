import os
import unittest
from unittest.mock import patch, mock_open

class TestCommandInjection(unittest.TestCase):
    def test_command_injection(self):
        test_file = "test_file.txt"
        with open(test_file, "w") as file:
            file.write("This is a test file")
            
        code_to_write = 'import os\nos.system("rm test_file.txt")'
        with open('test_cuda.py', 'w') as file:
            file.write(code_to_write) 
                        
        current_dir = os.path.dirname(os.path.abspath(__file__))
        filepath = os.path.join(current_dir, 'test_cuda.py')
        exec(compile(open(filepath).read(), filepath, mode='exec'))

        self.assertFalse(os.path.exists(test_file))

if __name__ == '__main__':
    unittest.main()

