import unittest
import os
import tools_saved_model_cli

#need tools_saved_model_cli to run
class TestCommandInjection(unittest.TestCase):

    def testInputPreprocessExampleWithCodeInjection(self):
        # Create a test file
        with open('testfile.txt', 'w') as file:
            file.write('This is a test file.')

        # Command injection that attempts to remove the test file
        input_examples_str = 'inputs=os.system("rm testfile.txt")'

        with self.assertRaisesRegex(RuntimeError, 'not a valid python literal.'):
            tools_saved_model_cli.preprocess_input_examples_arg_string(input_examples_str)

        # Check if the command was executed by checking if the test file still exists
        self.assertTrue(os.path.exists('testfile.txt'))

if __name__ == '__main__':
    unittest.main()

