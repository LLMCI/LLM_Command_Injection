def run_process_no_exception(code, env=None):
        import subprocess

        popen = subprocess.Popen(
            [sys.executable, '-c', code],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=env)
        (stdout, stderr) = popen.communicate()
        return (stdout, stderr)

