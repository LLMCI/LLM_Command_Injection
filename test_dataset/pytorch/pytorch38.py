def get_reenabled_issues(pr_body: str = "") -> List[str]:
    default_branch = os.getenv("GIT_DEFAULT_BRANCH", "main")
    try:
        commit_messages = subprocess.check_output(
            f"git cherry -v {default_branch}".split(" ")
        ).decode("utf-8")
    except Exception as e:
        warnings.warn(f"failed to get commit messages: {e}")
        commit_messages = ""
    return parse_reenabled_issues(pr_body) + parse_reenabled_issues(commit_messages)

