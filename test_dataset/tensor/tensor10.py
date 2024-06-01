def exec_test_function():
  # The point is to test A-normal form conversion of exec
  # pylint: disable=exec-used
  exec('computed' + 5 + 'stuff', globals(), locals())
