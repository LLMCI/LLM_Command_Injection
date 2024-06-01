if __name__ == "__main__":
    if "USE_CUDA" in os.environ and os.environ["USE_CUDA"] == "1":
        TESTS = COMMON_TESTS + GPU_TESTS
    else:
        TESTS = COMMON_TESTS
    for description, python_commands in TESTS:
        print(description)
        command_args = ["python", "-c", python_commands]
        command_string = " ".join(command_args)
        print("Command:", command_string)
        try:
            subprocess.check_call(command_args)
        except subprocess.CalledProcessError as e:
            sdk_root = os.environ.get(
                "WindowsSdkDir", "C:\\Program Files (x86)\\Windows Kits\\10"
            )
            debugger = os.path.join(sdk_root, "Debuggers", "x64", "cdb.exe")
            if os.path.exists(debugger):
                command_args = [debugger, "-o", "-c", "~*g; q"] + command_args
                command_string = " ".join(command_args)
                print("Reruning with traceback enabled")
                print("Command:", command_string)
                subprocess.run(command_args, check=False)
            sys.exit(e.returncode)
