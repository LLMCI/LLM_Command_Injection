def main(unused_argv):
  merged_source = pathlib.Path(tempfile.mkdtemp())
  shutil.copytree(SOURCE_PATH, merged_source / 'java')

  if FLAGS.gen_ops:
    # `$ yes | configure`
    yes = subprocess.Popen(['yes', ''], stdout=subprocess.PIPE)
    configure = subprocess.Popen([TENSORFLOW_ROOT / 'configure'],
                                 stdin=yes.stdout,
                                 cwd=TENSORFLOW_ROOT)
    configure.communicate()

    subprocess.check_call(
        ['bazel', 'build', '//tensorflow/java:java_op_gen_sources'],
        cwd=TENSORFLOW_ROOT)
    shutil.copytree(OP_SOURCE_PATH, merged_source / 'java/org/tensorflow/ops')

  gen_java.gen_java_docs(
      package='org.tensorflow',
      source_path=merged_source / 'java',
      output_dir=pathlib.Path(FLAGS.output_dir),
      site_path=pathlib.Path(FLAGS.site_path))
