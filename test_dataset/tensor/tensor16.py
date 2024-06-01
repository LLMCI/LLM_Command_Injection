def main():
  """This script runs the pip smoke test.

  Raises:
    RuntimeError: If any dependencies for py_tests exist in subSet

  Prerequisites:
      1. Bazel is installed.
      2. Running in github repo of tensorflow.
      3. Configure has been run.

  """

  # pip_package_dependencies_list is the list of included files in pip packages
  pip_package_dependencies = subprocess.check_output([
      "bazel", "cquery", "--experimental_cc_shared_library",
      PIP_PACKAGE_QUERY_EXPRESSION
  ])
  if isinstance(pip_package_dependencies, bytes):
    pip_package_dependencies = pip_package_dependencies.decode("utf-8")
  pip_package_dependencies_list = pip_package_dependencies.strip().split("\n")
  pip_package_dependencies_list = [
      x.split()[0] for x in pip_package_dependencies_list
  ]
  print("Pip package superset size: %d" % len(pip_package_dependencies_list))

  # tf_py_test_dependencies is the list of dependencies for all python
  # tests in tensorflow
  tf_py_test_dependencies = subprocess.check_output([
      "bazel", "cquery", "--experimental_cc_shared_library",
      PY_TEST_QUERY_EXPRESSION
  ])
  if isinstance(tf_py_test_dependencies, bytes):
    tf_py_test_dependencies = tf_py_test_dependencies.decode("utf-8")
  tf_py_test_dependencies_list = tf_py_test_dependencies.strip().split("\n")
  tf_py_test_dependencies_list = [
      x.split()[0] for x in tf_py_test_dependencies.strip().split("\n")
  ]
  print("Pytest dependency subset size: %d" % len(tf_py_test_dependencies_list))

  missing_dependencies = []
  # File extensions and endings to ignore
  ignore_extensions = [
      "_test", "_test.py", "_test_cpu", "_test_cpu.py", "_test_gpu",
      "_test_gpu.py", "_test_lib"
  ]

  ignored_files_count = 0
  denylisted_dependencies_count = len(DEPENDENCY_DENYLIST)
  # Compare dependencies
  for dependency in tf_py_test_dependencies_list:
    if dependency and dependency.startswith("//tensorflow"):
      ignore = False
      # Ignore extensions
      if any(dependency.endswith(ext) for ext in ignore_extensions):
        ignore = True
        ignored_files_count += 1

      # Check if the dependency is in the pip package, the dependency denylist,
      # or should be ignored because of its file extension.
      if not (ignore or dependency in pip_package_dependencies_list or
              dependency in DEPENDENCY_DENYLIST):
        missing_dependencies.append(dependency)

  print("Ignored files count: %d" % ignored_files_count)
  print("Denylisted dependencies count: %d" % denylisted_dependencies_count)
  if missing_dependencies:
    print("Missing the following dependencies from pip_packages:")
    for missing_dependency in missing_dependencies:
      print("\nMissing dependency: %s " % missing_dependency)
      print("Affected Tests:")
      rdep_query = ("rdeps(kind(py_test, %s), %s)" %
                    (" + ".join(PYTHON_TARGETS), missing_dependency))
      affected_tests = subprocess.check_output(
          ["bazel", "cquery", "--experimental_cc_shared_library", rdep_query])
      affected_tests_list = affected_tests.split("\n")[:-2]
      print("\n".join(affected_tests_list))

    raise RuntimeError("""
    One or more added test dependencies are not in the pip package.
If these test dependencies need to be in TensorFlow pip package, please add them to //tensorflow/tools/pip_package/BUILD.
Else add no_pip tag to the test.""")

  else:
    print("TEST PASSED")
