def testGeneratesStacktrace(self):
    if FLAGS.child:
      return

    # Subprocess sys.argv[0] with --child=True
    if sys.executable:
      child_process = subprocess.Popen(
          [sys.executable, sys.argv[0], '--child=True'], cwd=os.getcwd(),
          stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    else:
      child_process = subprocess.Popen(
          [sys.argv[0], '--child=True'], cwd=os.getcwd(),
          stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Capture its output. capture both stdout and stderr and append them.
    # We are not worried about timing or order of messages in this test.
    child_stdout, child_stderr = child_process.communicate()
    child_output = child_stdout + child_stderr

    # Make sure the child process is dead before we proceed.
    child_process.wait()

    logging.info('Output from the child process:')
    logging.info(child_output)

    # Verify a stack trace is printed.
    self.assertIn(b'PyEval_EvalFrame', child_output)

