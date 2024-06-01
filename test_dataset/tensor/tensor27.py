import ast


def run_user_main(wrapped_test_module):
  tree = ast.parse(tf_inspect.getsource(wrapped_test_module))

  target = ast.dump(ast.parse('if __name__ == "__main__": pass').body[0].test)

  for expr in reversed(tree.body):
    if isinstance(expr, ast.If) and ast.dump(expr.test) == target:
      break
  else:
    raise NotImplementedError(
        f'Could not find `if __name__ == "main":` block in {wrapped_test_module.__name__}.'
        )

  new_ast = ast.Module(body=expr.body, type_ignores=[])  
  exec(  
      compile(new_ast, '<ast>', 'exec'),
      globals(),
      wrapped_test_module.__dict__,
  )
