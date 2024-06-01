def get_git_diff_stdout() -> str:
  """Run git diff with appropriate arguments and capture stdout as a str."""
  proc = subprocess.run(
      ["git", "diff", "origin/main", "HEAD"],
      capture_output=True,
      check=True,
      text=True,
  )
  return proc.stdout
