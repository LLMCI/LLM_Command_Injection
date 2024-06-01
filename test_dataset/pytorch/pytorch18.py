def rebase_ghstack_onto(
    pr: GitHubPR, repo: GitRepo, onto_branch: str, dry_run: bool = False
) -> bool:
    if (
        subprocess.run(
            [sys.executable, "-m", "ghstack", "--help"],
            capture_output=True,
            check=False,
        ).returncode
        != 0
    ):
        subprocess.run([sys.executable, "-m", "pip", "install", "ghstack"], check=True)
    orig_ref = f"{re.sub(r'/head$', '/orig', pr.head_ref())}"

    repo.fetch(orig_ref, orig_ref)
    repo._run_git("rebase", onto_branch, orig_ref)

    if repo.rev_parse(orig_ref) == repo.rev_parse(onto_branch):
        raise Exception(SAME_SHA_ERROR)
