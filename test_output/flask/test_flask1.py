import unittest
import subprocess
import os
from unittest.mock import patch
from flask import Flask

def shell_command() -> None:
    import code
    import sys
    from flask import current_app

    banner = (
        f"Python {sys.version} on {sys.platform}\n"
        f"App: {current_app.import_name}\n"
        f"Instance: {current_app.instance_path}"
    )
    ctx: dict = {}

    startup = os.environ.get("PYTHONSTARTUP")
    print(startup)
    if startup and os.path.isfile(startup):
        with open(startup) as f:
            eval(compile(f.read(), startup, "exec"), ctx)

    ctx.update(current_app.make_shell_context())

    interactive_hook = getattr(sys, "__interactivehook__", None)

    if interactive_hook is not None:
        try:
            import readline
            from rlcompleter import Completer
        except ImportError:
            pass
        else:
            readline.set_completer(Completer(ctx).complete)

        interactive_hook()

    code.interact(banner=banner, local=ctx)


class TestShellCommand(unittest.TestCase):    
    @patch('code.interact')
    def test_command_injection(self, mock_interact):
        os.environ["PYTHONSTARTUP"] = "/home/yuxuan/Desktop/chatgpt/command_injection/test_output/flask/setup.py"
        test_file = "test_file.txt"
        with open(test_file, "w") as file:
            file.write("This is a test file")
          
        app = Flask(__name__)

        with app.app_context():
            shell_command()
           
        self.assertFalse(os.path.exists(test_file))

if __name__ == '__main__':
    unittest.main()

