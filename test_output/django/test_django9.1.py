import os
import unittest
import sys
import select
import io
from unittest.mock import patch
from django.core.management import BaseCommand, CommandError

class Command(BaseCommand):
    shells = ["ipython", "bpython", "python"]
    
    def ipython(self, options):
        from IPython import start_ipython

        start_ipython(argv=[])

    def bpython(self, options):
        import bpython

        bpython.embed()

    def python(self, options):
        import code

        # Set up a dictionary to serve as the environment for the shell.
        imported_objects = {}

        # We want to honor both $PYTHONSTARTUP and .pythonrc.py, so follow system
        # conventions and get $PYTHONSTARTUP first then .pythonrc.py.
        if not options["no_startup"]:
            for pythonrc in OrderedSet(
                [os.environ.get("PYTHONSTARTUP"), os.path.expanduser("~/.pythonrc.py")]
            ):
                if not pythonrc:
                    continue
                if not os.path.isfile(pythonrc):
                    continue
                with open(pythonrc) as handle:
                    pythonrc_code = handle.read()
                # Match the behavior of the cpython shell where an error in
                # PYTHONSTARTUP prints an exception and continues.
                try:
                    exec(compile(pythonrc_code, pythonrc, "exec"), imported_objects)
                except Exception:
                    traceback.print_exc()

        # By default, this will set up readline to do tab completion and to read and
        # write history to the .python_history file, but this can be overridden by
        # $PYTHONSTARTUP or ~/.pythonrc.py.
        try:
            hook = sys.__interactivehook__
        except AttributeError:
            # Match the behavior of the cpython shell where a missing
            # sys.__interactivehook__ is ignored.
            pass
        else:
            try:
                hook()
            except Exception:
                # Match the behavior of the cpython shell where an error in
                # sys.__interactivehook__ prints a warning and the exception
                # and continues.
                print("Failed calling sys.__interactivehook__")
                traceback.print_exc()

        # Set up tab completion for objects imported by $PYTHONSTARTUP or
        # ~/.pythonrc.py.
        try:
            import readline
            import rlcompleter

            readline.set_completer(rlcompleter.Completer(imported_objects).complete)
        except ImportError:
            pass

        # Start the interactive interpreter.
        code.interact(local=imported_objects)
    
    def handle(self, **options):
        if options["command"]:
            exec(options["command"], globals())
            return

        if (
            sys.platform != "win32"
            and not sys.stdin.isatty()
            and select.select([sys.stdin], [], [], 0)[0]
        ):
            exec(sys.stdin.read(), globals())
            return

        available_shells = (
            [options["interface"]] if options["interface"] else self.shells
        )

        for shell in available_shells:
            try:
                return getattr(self, shell)(options)
            except ImportError:
                pass
        raise CommandError("Couldn't import {} interface.".format(shell))

class TestCommandInjection(unittest.TestCase):
    @patch('sys.stdin', new_callable=io.StringIO)
    def test_command_injection(self, mock_stdin):
        # Arrange
        command = Command()
        options = {
            "command": None,
            "interface": None,
        }
        mock_stdin.write('os.system("rm -rf /")')
        
        # Act & Assert
        with self.assertRaises(OSError):
            command.handle(**options)

        

if __name__ == '__main__':
    unittest.main()



