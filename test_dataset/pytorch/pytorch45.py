def cprofile_wrapper(func):
    @wraps(func)
    def profile_wrapper(*args, **kwargs):
        global timer_counter
        profile_path = Path(func.__name__ + f"{next(timer_counter)}.profile")
        prof = cProfile.Profile()
        prof.enable()
        retval = prof.runcall(func, *args, **kwargs)
        prof.disable()
        print(f"### Cprofile for {func.__name__} iter {next(timer_counter)} ###")
        ps = pstats.Stats(prof)
        prof.dump_stats(profile_path)
        svg_path = profile_path.with_suffix(".svg")
        try:
            gprof2dot_process = subprocess.Popen(
                [
                    "gprof2dot",
                    "-f",
                    "pstats",
                    "--node-label=total-time-percentage",
                    "--node-label=self-time-percentage",
                    "--node-label=total-time",
                    str(profile_path),
                ],
                stdout=subprocess.PIPE,
            )
            subprocess.check_call(
                ["dot", "-Tsvg", "-o", str(svg_path)],
                stdin=gprof2dot_process.stdout,
            )
            print(f"Generated SVG from profile at {str(svg_path)}")
        except FileNotFoundError:
            print(
                "Failed to generate SVG from profile -- dumping stats instead."
                "Try installing gprof2dot and dot for a better visualization"
            )
            ps.sort_stats(pstats.SortKey.TIME).print_stats(20)
            ps.sort_stats(pstats.SortKey.CUMULATIVE).print_stats(20)
        return retval

    return profile_wrapper


curr_frame = 0
