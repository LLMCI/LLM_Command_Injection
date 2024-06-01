def test_pwd_command() -> None:
    """Test correct functionality."""
    session = BashProcess()
    commands = ["pwd"]
    output = session.run(commands)

    assert output == subprocess.check_output("pwd", shell=True).decode()


@pytest.mark.skip(reason="flaky on GHA, TODO to fix")
@pytest.mark.skipif(
    sys.platform.startswith("win"), reason="Test not supported on Windows"
)
def test_pwd_command_persistent() -> None:
    """Test correct functionality when the bash process is persistent."""
    session = BashProcess(persistent=True, strip_newlines=True)
    commands = ["pwd"]
    output = session.run(commands)

    assert subprocess.check_output("pwd", shell=True).decode().strip() in output

    session.run(["cd .."])
    new_output = session.run(["pwd"])
    # Assert that the new_output is a parent of the old output
    assert Path(output).parent == Path(new_output)
