def _check_python_output(cls, program) -> str:
        return subprocess.check_output(
            [sys.executable, "-W", "all", "-c", program],
            stderr=subprocess.STDOUT,
            # On Windows, opening the subprocess with the default CWD makes `import torch`
            # fail, so just set CWD to this script's directory
            cwd=os.path.dirname(os.path.realpath(__file__)),).decode("utf-8")
