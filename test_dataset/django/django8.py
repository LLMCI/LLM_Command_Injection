def run_formatters(written_files, black_path=(sentinel := object())):
    """
    Run the black formatter on the specified files.
    """
    # Use a sentinel rather than None, as which() returns None when not found.
    if black_path is sentinel:
        black_path = shutil.which("black")
    if black_path:
        subprocess.run(
            [black_path, "--fast", "--", *written_files],
            capture_output=True,
        )
