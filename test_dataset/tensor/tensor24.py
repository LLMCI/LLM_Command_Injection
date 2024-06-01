import os
import re
import subprocess
from shutil import which


def _get_ld_config_paths():
  """Returns all directories from 'ldconfig -p'."""
  ldconfig_path = which("ldconfig") or "/sbin/ldconfig"
  output = subprocess.check_output([ldconfig_path, "-p"])
  pattern = re.compile(".* => (.*)")
  result = set()
  for line in output.splitlines():
    try:
      match = pattern.match(line.decode("ascii"))
    except UnicodeDecodeError:
      match = False
    if match:
      result.add(os.path.dirname(match.group(1)))
  return sorted(list(result))
