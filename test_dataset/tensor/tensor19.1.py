def _Write(self, data, output_file):
    
    _, extension = os.path.splitext(output_file)
    with TemporaryDirectoryResource() as tempdir:
      if extension == ".json":
        json.dump(data, open(output_file, "w"), sort_keys=True, indent=2)
      elif extension in [".tflite", ".bin"]:
        input_json = os.path.join(tempdir, "temp.json")
        with open(input_json, "w") as fp:
          json.dump(data, fp, sort_keys=True, indent=2)
        returncode = subprocess.call([
            self._flatc_path, "-b", "--defaults-json", "--strict-json", "-o",
            tempdir, self._new_schema, input_json
        ])
        if returncode != 0:
          raise RuntimeError("flatc failed to convert upgraded json to binary.")

        shutil.copy(os.path.join(tempdir, "temp.tflite"), output_file)
      else:
        raise ValueError("Invalid extension on output file %r" % output_file)
