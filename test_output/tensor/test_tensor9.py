import unittest
import os
import re

_DUMP_TENSOR_PATTERN = re.compile(r"`.*?`")

class ExpressionEvaluator(object):
  """Evaluates Python expressions using debug tensor values from a dump."""

  def __init__(self, dump):
    """Constructor of ExpressionEvaluator.

    Args:
      dump: an instance of `DebugDumpDir`.
    """
    self._dump = dump
    self._cached_tensor_values = {}

  def evaluate(self, expression):
    """Parse an expression.

    Args:
      expression: the expression to be parsed.

    Returns:
      The result of the evaluation.

    Raises:
      ValueError: If the value of one or more of the debug tensors in the
        expression are not available.
    """
    dump_tensors_iter = re.finditer(_DUMP_TENSOR_PATTERN, expression)
    rewritten_expression = expression
    for match in reversed(list(dump_tensors_iter)):
      tensor_name = match.group(0)[1:-1].strip()
      rewritten_expression = (
          rewritten_expression[:match.start(0)] +
          "self._cached_tensor_values['" + tensor_name + "']" +
          rewritten_expression[match.end(0):])

    return eval(rewritten_expression)  # pylint: disable=eval-used


class TestCommandInjection(unittest.TestCase):
    def setUp(self):
        self.evaluator = ExpressionEvaluator(None)
        self.test_file = "test_file.txt"
        with open(self.test_file, "w") as file:
            file.write("This is a test file.")

    def test_command_injection(self):
        malicious_input = f"os.remove('{self.test_file}')"
        self.evaluator.evaluate(malicious_input)
        self.assertFalse(os.path.exists(self.test_file))

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)


if __name__ == "__main__":
    unittest.main()
