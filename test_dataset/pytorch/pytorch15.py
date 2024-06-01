import argparse
import json
import os
import pathlib
import subprocess
import sys
import urllib

CSV_LINTER = str(
    pathlib.Path(__file__).absolute().parent.parent.parent.parent
    / "tools/linter/adapters/no_merge_conflict_csv_linter.py"
)


def apply_lints(filename):
    patch = json.loads(subprocess.check_output([sys.executable, CSV_LINTER, filename]))
    if patch.get("replacement"):
        with open(filename) as fd:
            data = fd.read().replace(patch["original"], patch["replacement"])
        with open(filename, "w") as fd:
            fd.write(data)
