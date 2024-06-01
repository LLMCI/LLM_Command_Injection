def build_headers(output_dir):
  """Builds the headers files for TF."""
  os.makedirs(output_dir, exist_ok=True)

  # `$ yes | configure`
  yes = subprocess.Popen(['yes', ''], stdout=subprocess.PIPE)
  configure = subprocess.Popen([TENSORFLOW_ROOT / 'configure'],
                               stdin=yes.stdout,
                               cwd=TENSORFLOW_ROOT)
  configure.communicate()

  subprocess.check_call(['bazel', 'build', 'tensorflow/cc:cc_ops'],
                        cwd=TENSORFLOW_ROOT)
  subprocess.check_call(
      ['cp', '--dereference', '-r', 'bazel-bin', output_dir / 'bazel-genfiles'],
      cwd=TENSORFLOW_ROOT)
