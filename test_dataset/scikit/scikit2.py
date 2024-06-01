def test_configure():
    # Smoke test `python setup.py config` command run at the root of the
    # scikit-learn source tree.
    # This test requires Cython which is not necessarily there when running
    # the tests of an installed version of scikit-learn or when scikit-learn
    # is installed in editable mode by pip build isolation enabled.
    pytest.importorskip("Cython")
    cwd = os.getcwd()
    setup_path = os.path.abspath(os.path.join(sklearn.__path__[0], ".."))
    setup_filename = os.path.join(setup_path, "setup.py")
    if not os.path.exists(setup_filename):
        pytest.skip("setup.py not available")
    try:
        os.chdir(setup_path)
        old_argv = sys.argv
        sys.argv = ["setup.py", "config"]

        with warnings.catch_warnings():
            # The configuration spits out warnings when not finding
            # Blas/Atlas development headers
            warnings.simplefilter("ignore", UserWarning)
            with open("setup.py") as f:
                exec(f.read(), dict(__name__="__main__"))
    finally:
        sys.argv = old_argv
        os.chdir(cwd)
