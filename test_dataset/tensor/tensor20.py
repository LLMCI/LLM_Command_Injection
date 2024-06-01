@dataclasses.dataclass
class ClangTidyCommand:
  file: str
  arguments: list[str]

  def to_invocation(self, extra_flags: Optional[list[str]] = None) -> list[str]:
    if extra_flags is None:
      extra_flags = []
    return ["clang-tidy", self.file, *extra_flags, "--", *self.arguments]


def run_commands(
    commands: list[ClangTidyCommand],
    changed_lines: Optional[list[JSONDict]],
) -> list[ClangTidyCommand]:

  failed = []
  logging.info("Found %d clang-tidy commands to run...", len(commands))
  for command in commands:
    if changed_lines:
      changed_lines_json = json.dumps(changed_lines)
      extra_flags = [f"--line_filter={changed_lines_json}"]
    else:
      extra_flags = []
    invocation = command.to_invocation(extra_flags=extra_flags)
    logging.debug("clang-tidy command:")
    sp = subprocess.run(invocation, check=False)
    if sp.returncode != 0:
      logging.error("clang-tidy invocation failed: %s", invocation)
      failed.append(command)

  return failed

