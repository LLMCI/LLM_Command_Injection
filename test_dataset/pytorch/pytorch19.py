def get_sha(pytorch_root: Union[str, Path]) -> str:
    try:
        return (
            subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=pytorch_root)
            .decode("ascii")
            .strip()
        )
    except Exception:
        return UNKNOWN


def get_tag(pytorch_root: Union[str, Path]) -> str:
    try:
        tag = subprocess.run(
            ["git", "describe", "--tags", "--exact"],
            cwd=pytorch_root,
            encoding="ascii",
            capture_output=True,
        ).stdout.strip()
        if RELEASE_PATTERN.match(tag):
            return tag
        else:
            return UNKNOWN
    except Exception:
        return UNKNOWN
