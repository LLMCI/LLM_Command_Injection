import unittest
import subprocess
import ast
import re
from contextlib import redirect_stdout
from io import StringIO
import os


def sanitize_input(query: str) -> str:
    # Removes `, whitespace & python from start
    query = re.sub(r"^(\s|`)*(?i:python)?\s*", "", query)
    # Removes whitespace & ` from end
    query = re.sub(r"(\s|`)*$", "", query)
    return query


class TestRun(unittest.TestCase):

    globals=None
    locals=None
    
    def test_command_injection(self):
        test_file="test_file.txt"
        with open(test_file, "w") as f:
            f.write("Hello")
        # Command injection payload
        payload = "import os; os.remove('/home/yuxuan/Desktop/chatgpt/command_injection/test_output/langchain/test_file.txt')"

        # Execute the command injection payload
        result = self._run(payload)

        # Check if the command is executed
        self.assertFalse(os.path.exists(test_file))
        
    def sanitize_input(query: str) -> str:
        # Removes `, whitespace & python from start
        query = re.sub(r"^(\s|`)*(?i:python)?\s*", "", query)
        # Removes whitespace & ` from end
        query = re.sub(r"(\s|`)*$", "", query)
        return query

    def _run(self, query):
        """Use the tool."""
        try:
            if self.sanitize_input:
                query = sanitize_input(query)
            tree = ast.parse(query)
            module = ast.Module(tree.body[:-1], type_ignores=[])
            exec(ast.unparse(module), self.globals, self.locals)  # type: ignore
            module_end = ast.Module(tree.body[-1:], type_ignores=[])
            module_end_str = ast.unparse(module_end)  # type: ignore
            io_buffer = StringIO()
            try:
                with redirect_stdout(io_buffer):
                    ret = eval(module_end_str, self.globals, self.locals)
                    if ret is None:
                        return io_buffer.getvalue()
                    else:
                        return ret
            except Exception:
                with redirect_stdout(io_buffer):
                    exec(module_end_str, self.globals, self.locals)
                return io_buffer.getvalue()
        except Exception as e:
            return "{}: {}".format(type(e).__name__, str(e))

if __name__ == '__main__':
    unittest.main()
