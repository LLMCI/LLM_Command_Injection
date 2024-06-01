def testInputPreprocessExampleWithCodeInjection(self):
    input_examples_str = 'inputs=os.system("echo hacked")'
    with self.assertRaisesRegex(RuntimeError, 'not a valid python literal.'):
      saved_model_cli.preprocess_input_examples_arg_string(input_examples_str)
