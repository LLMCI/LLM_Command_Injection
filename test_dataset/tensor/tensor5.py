def get_gcc_version(self):
    gcc_major_version = 0
    gcc_minor_version = 0
    # check to see if gcc is present
    gcc_path = ""
    gcc_path_cmd = "command -v gcc"
    try:
      gcc_path = subprocess.check_output(gcc_path_cmd, shell=True,
                                         stderr=subprocess.STDOUT).\
        strip()
      print("gcc located here: {}".format(gcc_path))
      if not os.access(gcc_path, os.F_OK | os.X_OK):
        raise ValueError(
            "{} does not exist or is not executable.".format(gcc_path))

      gcc_output = subprocess.check_output(
          [gcc_path, "-dumpfullversion", "-dumpversion"],
          stderr=subprocess.STDOUT).strip()
      # handle python2 vs 3 (bytes vs str type)
      if isinstance(gcc_output, bytes):
        gcc_output = gcc_output.decode("utf-8")
      print("gcc version: {}".format(gcc_output))
      gcc_info = gcc_output.split(".")
      gcc_major_version = int(gcc_info[0])
      gcc_minor_version = int(gcc_info[1])
    except subprocess.CalledProcessException as e:
      print("Problem getting gcc info: {}".format(e))
      gcc_major_version = 0
      gcc_minor_version = 0
    return gcc_major_version, gcc_minor_version
