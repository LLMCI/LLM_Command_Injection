def load_op_library(library_filename):
  lib_handle = py_tf.TF_LoadLibrary(library_filename)
  try:
    wrappers = _pywrap_python_op_gen.GetPythonWrappers(
        py_tf.TF_GetOpList(lib_handle))
  finally:
    # Delete the library handle to release any memory held in C
    # that are no longer needed.
    py_tf.TF_DeleteLibraryHandle(lib_handle)

  # Get a unique name for the module.
  module_name = hashlib.sha1(wrappers).hexdigest()
  if module_name in sys.modules:
    return sys.modules[module_name]
  module_spec = importlib.machinery.ModuleSpec(module_name, None)
  module = importlib.util.module_from_spec(module_spec)
  # pylint: disable=exec-used
  exec(wrappers, module.__dict__)
  # Allow this to be recognized by AutoGraph.
  setattr(module, '_IS_TENSORFLOW_PLUGIN', True)
  sys.modules[module_name] = module
  return module
