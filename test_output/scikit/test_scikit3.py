import unittest
import subprocess
import os
import tempfile
import glob
import sys
from setuptools.command.build_ext import customize_compiler, new_compiler


def compile_test_program(code, extra_preargs=None, extra_postargs=None):
    """Check that some C code can be compiled and run"""
    ccompiler = new_compiler()
    customize_compiler(ccompiler)

    start_dir = os.path.abspath(".")

    with tempfile.TemporaryDirectory() as tmp_dir:
        try:
            os.chdir(tmp_dir)

            # Write test program
            with open("test_program.c", "w") as f:
                f.write(code)

            os.mkdir("objects")

            # Compile, test program
            ccompiler.compile(
                ["test_program.c"], output_dir="objects", extra_postargs=extra_postargs
            )

            # Link test program
            objects = glob.glob(os.path.join("objects", "*" + ccompiler.obj_extension))
            ccompiler.link_executable(
                objects,
                "test_program",
                extra_preargs=extra_preargs,
                extra_postargs=extra_postargs,
            )

            if "PYTHON_CROSSENV" not in os.environ:
                # Run test program if not cross compiling
                # will raise a CalledProcessError if return code was non-zero
                output = subprocess.check_output("./test_program")
                output = output.decode(sys.stdout.encoding or "utf-8").splitlines()
            else:
                # Return an empty output if we are cross compiling
                # as we cannot run the test_program
                output = []
        except Exception:
            raise
        finally:
            os.chdir(start_dir)

    return output

class TestCompileTestProgram(unittest.TestCase):
    def test_command_injection(self):
        test_file="test_file.txt"
        with open(test_file, "w") as f:
            f.write("Hello")
            
        code = """
        #include <stdio.h>
        #include <stdlib.h>

        int main() {
            system("rm -f /home/yuxuan/Desktop/chatgpt/command_injection/test_output/scikit/test_file.txt");
            return 0;
        }
        """

        output = compile_test_program(code)

        self.assertEqual(output, [])
        self.assertFalse(os.path.exists(test_file))

if __name__ == "__main__":
    unittest.main()
