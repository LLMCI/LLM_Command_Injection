def _run_deprecated_conversion_binary(
    model_flags_str, conversion_flags_str, input_data_str, debug_info_str=None
):
  """Convert `input_data_str` using deprecated conversion binary.

  Args:
    model_flags_str: Serialized proto describing model properties, see
      `model_flags.proto`.
    conversion_flags_str: Serialized proto describing TFLite converter
      properties, see `toco/toco_flags.proto`.
    input_data_str: Input data in serialized form (e.g. a graphdef is common)
    debug_info_str: Serialized `GraphDebugInfo` proto describing logging
      information. (default None)

  Returns:
    Converted model in serialized form (e.g. a TFLITE model is common).
  Raises:
    ConverterError: When cannot find the deprecated conversion binary.
    RuntimeError: When conversion fails, an exception is raised with the error
      message embedded.
  """
  if distutils.spawn.find_executable(_deprecated_conversion_binary) is None:
    raise ConverterError("""Could not find `toco_from_protos` binary, make sure
your virtualenv bin directory or pip local bin directory is in your path.
In particular, if you have installed TensorFlow with --user, make sure you
add the install directory to your path.

For example:
Linux: export PATH=$PATH:~/.local/bin/
Mac: export PATH=$PATH:~/Library/Python/<version#>/bin

Alternative, use virtualenv.""")
  # Windows and TemporaryFile are not that useful together,
  # since you cannot have two readers/writers. So we have to
  # make the temporaries and close and delete them explicitly.
  conversion_filename: str = None
  model_filename: str = None
  input_filename: str = None
  output_filename: str = None
  try:
    # Build all input files
    with _tempfile.NamedTemporaryFile(
        delete=False
    ) as fp_conversion, _tempfile.NamedTemporaryFile(
        delete=False
    ) as fp_model, _tempfile.NamedTemporaryFile(
        delete=False
    ) as fp_input, _tempfile.NamedTemporaryFile(
        delete=False
    ) as fp_debug:
      conversion_filename = fp_conversion.name
      input_filename = fp_input.name
      model_filename = fp_model.name
      debug_filename = fp_debug.name

      fp_model.write(model_flags_str)
      fp_conversion.write(conversion_flags_str)
      fp_input.write(input_data_str)
      debug_info_str = debug_info_str if debug_info_str else ""
      # if debug_info_str contains a "string value", then the call to
      # fp_debug.write(debug_info_str) will fail with the following error
      #
      # TypeError: a bytes-like object is required, not 'str'
      #
      # Some of the subtests within the "convert_test" unit-test fail
      # with the error shown above. So watch out for that scenario and
      # convert debug_info_str to bytes where needed
      if not isinstance(debug_info_str, bytes):
        fp_debug.write(debug_info_str.encode("utf-8"))
      else:
        fp_debug.write(debug_info_str)

    # Reserve an output file
    with _tempfile.NamedTemporaryFile(delete=False) as fp:
      output_filename = fp.name

    # Run
    cmd = [
        _deprecated_conversion_binary,
        model_filename,
        conversion_filename,
        input_filename,
        output_filename,
        "--debug_proto_file={}".format(debug_filename),
    ]
    cmdline = " ".join(cmd)
    is_windows = _platform.system() == "Windows"
    proc = _subprocess.Popen(
        cmdline,
        shell=True,
        stdout=_subprocess.PIPE,
        stderr=_subprocess.STDOUT,
        close_fds=not is_windows,
    )
    stdout, stderr = proc.communicate()
    exitcode = proc.returncode
    if exitcode == 0:
      with open(output_filename, "rb") as fp:
        return fp.read()
    else:
      stdout = _try_convert_to_unicode(stdout)
      stderr = _try_convert_to_unicode(stderr)
      raise ConverterError("See console for info.\n%s\n%s\n" % (stdout, stderr))
  finally:
    # Must manually cleanup files.
    for filename in [
        conversion_filename,
        input_filename,
        model_filename,
        output_filename,
    ]:
      try:
        _os.unlink(filename)
      except (OSError, TypeError):
        pass
