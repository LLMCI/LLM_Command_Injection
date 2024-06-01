def run_shell_cmd(args):
  """Executes shell commands and returns output.

  Args:
    args: String of shell commands to run.

  Returns:
    Tuple output (stdoutdata, stderrdata) from running the shell commands.
  """
  proc = subprocess.Popen(
      args,
      shell=True,
      stdout=subprocess.PIPE,
      stderr=subprocess.STDOUT
  )
  return proc.communicate()

