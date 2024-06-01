def create_dummy_module_and_function():
    module = types.ModuleType("dummy_module")
    module.__spec__ = importlib.machinery.ModuleSpec(
        "dummy_module", None, origin=os.path.abspath(__file__)
    )
    exec(module_code, module.__dict__)
    sys.modules["dummy_module"] = module
    # Need to override the original function since its __code__.co_filename is not a regular python file name,
    # and the skipfiles rules use filename when checking SKIP_DIRS.
    module.add = add
    return module, module.add
