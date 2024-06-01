import inspect
import os
import subprocess
import sys
from functools import partial
from operator import attrgetter

REVISION_CMD = "git rev-parse --short HEAD"


def _get_git_revision():
    try:
        revision = subprocess.check_output(REVISION_CMD.split()).strip()
    except (subprocess.CalledProcessError, OSError):
        print("Failed to execute git to get revision")
        return None
    return revision.decode("utf-8")
