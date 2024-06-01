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
