def mlir_convert_file(graph_def_filename,
                      input_tensors,
                      output_tensors,
                      quantization_params=None,
                      additional_flags=""):
  bin_path = resource_loader.get_path_to_datafile(
      "../../../../compiler/mlir/lite/tf_tfl_translate")

  with tempfile.NamedTemporaryFile() as output_file, \
       tempfile.NamedTemporaryFile("w+") as stdout_file:
    input_shapes = []
    for input_tensor in input_tensors:
      shape = input_tensor[1]
      input_shapes.append(",".join([str(dim) for dim in shape]))
    input_shapes_str = ":".join(input_shapes)

    input_types = ",".join([x[2] for x in input_tensors])

    quant_flags = ""
    if quantization_params is not None:
      min_vals = ",".join([str(val) for val in quantization_params[1]])
      max_vals = ",".join([str(val) for val in quantization_params[2]])
      quant_flags = ("-tf-inference-type=" + quantization_params[0] +
                     " -tf-input-min-values='" + min_vals +
                     "' -tf-input-max-values='" + max_vals + "' " +
                     "-emit-quant-adaptor-ops ")
    cmd = ("%s -tf-input-arrays=%s -tf-input-data-types=%s -tf-input-shapes=%s "
           "-tf-output-arrays=%s " + quant_flags + additional_flags +
           "%s -o %s")
    cmd = cmd % (
        bin_path,
        ",".join([x[0] for x in input_tensors]),
        input_types,
        input_shapes_str,
        ",".join(output_tensors),
        graph_def_filename,
        output_file.name,
    )
    exit_code = os.system(cmd)
    log = (
        cmd + "exited with code %d" % exit_code + "\n------------------\n" +
        stdout_file.read())
    return (None if exit_code != 0 else output_file.read()), log
