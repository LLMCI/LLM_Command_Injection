def run(args: List[str], **kwargs: Any) -> Tuple[CompletedProcessType, str]:
            # https://thraxil.org/users/anders/posts/2008/03/13/Subprocess-Hanging-PIPE-is-your-enemy/
            f_stdout_stderr = open(stdout_stderr_log, "wb")
            try:
                invocation = subprocess.run(
                    args,
                    stdout=f_stdout_stderr,
                    stderr=subprocess.STDOUT,
                    **kwargs,
                )
                with open(stdout_stderr_log) as f:
                    return invocation, f.read()
            finally:
                f_stdout_stderr.close()
