if __name__ == "__main__":
    ret = subprocess.run(
        sys.argv[1:], stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr
    )

    depfile_path = None
    include_dirs = []
