def main() -> int:
  # Setup logging
  logging.basicConfig()
  logging.getLogger().setLevel(logging.INFO)

  # Parse arguments
  parser = argparse.ArgumentParser(description="Run clang-tidy on XLA.")
  parser.add_argument(
      "--changed_lines_only", action=argparse.BooleanOptionalAction
  )
  args = parser.parse_args(sys.argv[1:])

  # Gather and run clang-tidy invocations
  logging.info("Reading `bazel aquery` output from stdin...")
  parsed_aquery_output = json.loads(sys.stdin.read())

  # Maybe make file_allowlist
  changed_lines = None
  if args.changed_lines_only:
    changed_lines = _changed_lines_from_git_diff()
    changed_files = [entry["name"] for entry in changed_lines]
    logging.info("Found changed files: %s", changed_files)

  # Need this symlink so that headers will be found
  subprocess.run(["ln", "-s", "bazel-xla/external", "external"], check=True)
  commands = extract_clang_tidy_commands(parsed_aquery_output)
  failed_invocations = run_commands(commands, changed_lines)
  subprocess.run("rm", "external", check=True)
  return 1 if failed_invocations else 0
