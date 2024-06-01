def get_from_config():
    """Get benchmarks configuration from the config.json file"""
    current_path = Path(__file__).resolve().parent

    config_path = current_path / "config.json"
    with open(config_path, "r") as config_file:
        config_file = "".join(line for line in config_file if line and "//" not in line)
        config = json.loads(config_file)

    profile = os.getenv("SKLBENCH_PROFILE", config["profile"])

    n_jobs_vals_env = os.getenv("SKLBENCH_NJOBS")
    if n_jobs_vals_env:
        n_jobs_vals = eval(n_jobs_vals_env)
    else:
        n_jobs_vals = config["n_jobs_vals"]
    if not n_jobs_vals:
        n_jobs_vals = list(range(1, 1 + cpu_count()))



