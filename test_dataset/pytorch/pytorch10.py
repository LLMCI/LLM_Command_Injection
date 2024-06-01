def _embed_libiomp(self):
        lib_dir = os.path.join(self.build_lib, "torch", "lib")
        libtorch_cpu_path = os.path.join(lib_dir, "libtorch_cpu.dylib")
        if not os.path.exists(libtorch_cpu_path):
            return
        # Parse libtorch_cpu load commands
        otool_cmds = (
            subprocess.check_output(["otool", "-l", libtorch_cpu_path])
            .decode("utf-8")
            .split("\n")
        )
        rpaths, libs = [], []
        for idx, line in enumerate(otool_cmds):
            if line.strip() == "cmd LC_LOAD_DYLIB":
                lib_name = otool_cmds[idx + 2].strip()
                assert lib_name.startswith("name ")
                libs.append(lib_name.split(" ", 1)[1].rsplit("(", 1)[0][:-1])

            if line.strip() == "cmd LC_RPATH":
                rpath = otool_cmds[idx + 2].strip()
                assert rpath.startswith("path ")
                rpaths.append(rpath.split(" ", 1)[1].rsplit("(", 1)[0][:-1])

        omp_lib_name = "libiomp5.dylib"
        if os.path.join("@rpath", omp_lib_name) not in libs:
            return

        # Copy libiomp5 from rpath locations
        for rpath in rpaths:
            source_lib = os.path.join(rpath, omp_lib_name)
            if not os.path.exists(source_lib):
                continue
            target_lib = os.path.join(self.build_lib, "torch", "lib", omp_lib_name)
            self.copy_file(source_lib, target_lib)
            break
