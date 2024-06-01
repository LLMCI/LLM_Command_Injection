import unittest
import os
import dis

def _eval_no_call(stmt, glob, loc):
    """Evaluate statement as long as it does not contain any method/function calls."""
    bytecode = compile(stmt, "", mode="eval")
    for insn in dis.get_instructions(bytecode):
        if "CALL" in insn.opname:
            raise RuntimeError(
                f"Type annotation should not contain calls, but '{stmt}' does"
            )
    return eval(bytecode, glob, loc)  # type: ignore[arg-type] # noqa: P204

class TestCommandInjection(unittest.TestCase):
    def setUp(self):
        self.test_file = "test_file.txt"
        with open(self.test_file, "w") as file:
            file.write("This is a test file.")

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_command_injection(self):
        malicious_code = f"os.remove('{self.test_file}')"
        
        _eval_no_call(malicious_code, {}, {})

        # Check if the file still exists, if it does, the command injection was unsuccessful
        self.assertFalse(os.path.exists(self.test_file))

if __name__ == "__main__":
    unittest.main()

