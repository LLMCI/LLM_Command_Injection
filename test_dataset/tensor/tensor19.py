class Converter:

   def __init__(self):
      paths_to_try = [
          "../../../../flatbuffers/flatc",  # not bazel
          "../../../../external/flatbuffers/flatc"  # bazel
      ]
      for p in paths_to_try:
        self._flatc_path = resource_loader.get_path_to_datafile(p)
        if os.path.exists(self._flatc_path): break


   def _Read(self, input_file, schema, raw_binary=False):
    
     raw_binary = ["--raw-binary"] if raw_binary else []
     with TemporaryDirectoryResource() as tempdir:
       basename = os.path.basename(input_file)
       basename_no_extension, extension = os.path.splitext(basename)
       if extension in [".bin", ".tflite"]:
         # Convert to json using flatc
         returncode = subprocess.call([
             self._flatc_path,
             "-t",
             "--strict-json",
             "--defaults-json",
         ] + raw_binary + ["-o", tempdir, schema, "--", input_file])
         if returncode != 0:
           raise RuntimeError("flatc failed to convert from binary to json.")
         json_file = os.path.join(tempdir, basename_no_extension + ".json")
         if not os.path.exists(json_file):
           raise RuntimeError("Could not find %r" % json_file)
       elif extension == ".json":
         json_file = input_file
       else:
         raise ValueError("Invalid extension on input file %r" % input_file)
       return json.load(open(json_file))
