import os
import select
import sys
import traceback

from django.core.management import BaseCommand, CommandError
from django.utils.datastructures import OrderedSet


class Command(BaseCommand):
    shells = ["ipython", "bpython", "python"]


    def handle(self, **options):
        # Execute the command and exit.
        if options["command"]:
            exec(options["command"], globals())
            return

        # Execute stdin if it has anything to read and exit.
        # Not supported on Windows due to select.select() limitations.
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
