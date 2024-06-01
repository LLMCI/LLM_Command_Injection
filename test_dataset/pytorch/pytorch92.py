def system(command):
    """Returns (return-code, stdout, stderr)"""
    print(f"[system] {command}")
    p = subprocess.Popen(
        command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True
    )
    output, err = p.communicate()
    rc = p.returncode
    output = output.decode("ascii")
    err = err.decode("ascii")
    return rc, output, err
