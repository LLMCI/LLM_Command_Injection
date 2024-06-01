def _lint_file(file_path: str) -> None:
    p = subprocess.Popen(["lintrunner", "-a", file_path])
    p.wait()