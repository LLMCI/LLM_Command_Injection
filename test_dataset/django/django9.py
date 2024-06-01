import os
import select
import sys
import traceback

from django.core.management import BaseCommand, CommandError
from django.utils.datastructures import OrderedSet


class Command(BaseCommand):

    def python(self, options):
        import code

        imported_objects = {}

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
                try:
                    exec(compile(pythonrc_code, pythonrc, "exec"), imported_objects)
                except Exception:
                    traceback.print_exc()

        try:
            hook = sys.__interactivehook__
        except AttributeError:
            pass
        else:
            try:
                hook()
            except Exception:
                print("Failed calling sys.__interactivehook__")
                traceback.print_exc()

        try:
            import readline
            import rlcompleter

            readline.set_completer(rlcompleter.Completer(imported_objects).complete)
        except ImportError:
            pass

        code.interact(local=imported_objects)
