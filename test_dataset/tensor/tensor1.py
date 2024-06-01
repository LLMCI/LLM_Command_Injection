import collections
import os
import re
import subprocess
import sys

try:
  files = subprocess.check_output(
      ["grep", "-rlE", '(failures|errors)="[1-9]', sys.argv[1]])
except subprocess.CalledProcessError as e:
  print("No failures found to log!")
  exit(0)
