def main() -> None:
    args = parse_args()

    branch_name = os.environ["NEW_BRANCH_NAME"]
    pr_num = None

    # query to see if a pr already exists
    params = {
        "q": f"is:pr is:open in:title author:pytorchupdatebot repo:{OWNER}/{REPO} {args.repo_name} hash update",
        "sort": "created",
    }
    response = git_api("/search/issues", params)
    if response["total_count"] != 0:
        # pr does exist
        pr_num = response["items"][0]["number"]
        link = response["items"][0]["html_url"]
        response = git_api(f"/repos/{OWNER}/{REPO}/pulls/{pr_num}", {})
        branch_name = response["head"]["ref"]
        print(
            f"pr does exist, number is {pr_num}, branch name is {branch_name}, link is {link}"
        )

    hash = (
        subprocess.run(
            f"git rev-parse {args.branch}".split(),
            capture_output=True,
            cwd=f"{args.repo_name}",
        )
        .stdout.decode("utf-8")
        .strip()
    )
    
