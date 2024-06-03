def get_commit_message():
    """Retrieve the commit message."""
    build_source_version_message = os.environ["BUILD_SOURCEVERSIONMESSAGE"]

    if os.environ["BUILD_REASON"] == "PullRequest":
        # By default pull requests use refs/pull/PULL_ID/merge as the source branch
        # which has a "Merge ID into ID" as a commit message. The latest commit
        # message is the second to last commit
        commit_id = build_source_version_message.split()[1]
        git_cmd = ["git", "log", commit_id, "-1", "--pretty=%B"]
        commit_message = subprocess.run(
            git_cmd, capture_output=True, text=True
        ).stdout.strip()
    else:
        commit_message = build_source_version_message