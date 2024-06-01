def check_for_lingering_string(lingering_string):
  """Check for given lingering strings."""
  formatted_string = lingering_string.replace(".", r"\.")
  try:
    linger_str_output = subprocess.check_output(
        ["grep", "-rnoH", formatted_string, TF_SRC_DIR])
    linger_strs = linger_str_output.decode("utf8").split("\n")
  except subprocess.CalledProcessError:
    linger_strs = []

  if linger_strs:
    print("WARNING: Below are potentially instances of lingering old version "
          "string \"%s\" in source directory \"%s/\" that are not "
          "updated by this script. Please check them manually!"
          % (lingering_string, TF_SRC_DIR))
    for linger_str in linger_strs:
      print(linger_str)
  else:
    print("No lingering old version strings \"%s\" found in source directory"
          " \"%s/\". Good." % (lingering_string, TF_SRC_DIR))
