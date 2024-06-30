from tensorflow.python.tools import saved_model_cli

def preprocess_input_exprs_arg_string(input_exprs_str, safe=True):
  input_dict = {}

  for input_raw in filter(bool, input_exprs_str.split(';')):
    if '=' not in input_exprs_str:
      raise RuntimeError('--input_exprs "%s" format is incorrect. Please follow'
                         '"<input_key>=<python expression>"' % input_exprs_str)
    input_key, expr = input_raw.split('=', 1)
    if safe:
      try:
        input_dict[input_key] = ast.literal_eval(expr)
      except Exception as exc:
        raise RuntimeError(
            f'Expression "{expr}" is not a valid python literal.') from exc
    else:
      # ast.literal_eval does not work with numpy expressions
      input_dict[input_key] = eval(expr)  # pylint: disable=eval-used
  return input_dict

def preprocess_input_examples_arg_string(input_examples_str):
    
  input_dict = preprocess_input_exprs_arg_string(input_examples_str)
  for input_key, example_list in input_dict.items():
    if not isinstance(example_list, list):
      raise ValueError(
          'tf.Example input must be a list of dictionaries, but "%s" is %s' %
          (example_list, type(example_list)))
    input_dict[input_key] = [
        _create_example_string(example) for example in example_list
    ]
  return input_dict

def testInputPreprocessExampleWithCodeInjection(self):
    input_examples_str = 'inputs=os.system("echo hacked")'
    with self.assertRaisesRegex(RuntimeError, 'not a valid python literal.'):
      saved_model_cli.preprocess_input_examples_arg_string(input_examples_str)
