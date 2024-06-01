def get_pytorch_folder() -> str:
    # TOOLS_FOLDER in oss: pytorch/tools/code_coverage
    return os.path.abspath(
        os.environ.get(
            "PYTORCH_FOLDER", os.path.join(TOOLS_FOLDER, os.path.pardir, os.path.pardir)
        )
    )

def get_gcda_files() -> List[str]:
    folder_has_gcda = os.path.join(get_pytorch_folder(), "build")
    if os.path.isdir(folder_has_gcda):
        # TODO use glob
        # output = glob.glob(f"{folder_has_gcda}/**/*.gcda")
        output = subprocess.check_output(["find", folder_has_gcda, "-iname", "*.gcda"])
        return output.decode("utf-8").split("\n")
    else:
        return []
