def get_git_version(git_base_path, git_tag_override):
  unknown_label = b"unknown"
  try:
    # Force to bytes so this works on python 2 and python 3
    val = bytes(
        subprocess.check_output([
            "git",
            str("--git-dir=%s/.git" % git_base_path),
            str("--work-tree=%s" % git_base_path), "describe", "--long",
            "--tags"
        ]).strip())
    version_separator = b"-"
    if git_tag_override and val:
      split_val = val.split(version_separator)
      if len(split_val) < 3:
        raise Exception(
            ("Expected git version in format 'TAG-COMMITS AFTER TAG-HASH' "
             "but got '%s'") % val)
      # There might be "-" in the tag name. But we can be sure that the final
      # two "-" are those inserted by the git describe command.
      abbrev_commit = split_val[-1]
      val = version_separator.join(
          [bytes(git_tag_override, "utf-8"), b"0", abbrev_commit])
    return val if val else unknown_label
  except (subprocess.CalledProcessError, OSError):
    return unknown_label
