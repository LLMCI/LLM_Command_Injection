def parse_args() -> Any:
    parser = ArgumentParser("Rebase PR into branch")
    parser.add_argument("--repo-name", type=str)
    parser.add_argument("--branch", type=str)
    parser.add_argument("--pin-folder", type=str)
    return parser.parse_args()

def main() -> None:
    args = parse_args()

    branch_name = os.environ["NEW_BRANCH_NAME"]
    pr_num = None

    hash = (
        subprocess.run(
            f"git rev-parse {args.branch}".split(),
            capture_output=True,
            cwd=f"{args.repo_name}",
        )
        .stdout.decode("utf-8")
        .strip()
    )
    
