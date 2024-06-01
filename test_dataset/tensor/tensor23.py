import os
import subprocess
from shutil import which


def check_cuda_lib(path, check_soname=True):
  """Tests if a library exists on disk and whether its soname matches the filename.

  Args:
    path: the path to the library.
    check_soname: whether to check the soname as well.

  Raises:
    Exception: If the library does not exist or if its soname does not match
    the filename.
  """
  if not os.path.isfile(path):
    raise Exception("No library found under: " + path)
  objdump = which("objdump")
  if check_soname and objdump is not None:
    # Decode is necessary as in py3 the return type changed from str to bytes
    output = subprocess.check_output([objdump, "-p", path]).decode("utf-8")
    output = [line for line in output.splitlines() if "SONAME" in line]
    sonames = [line.strip().split(" ")[-1] for line in output]
    if not any(soname == os.path.basename(path) for soname in sonames):
      raise Exception("None of the libraries match their SONAME: " + path)
