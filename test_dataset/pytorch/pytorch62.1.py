def get_rocm_version():
    from torch.torch_version import TorchVersion
    from torch.utils import cpp_extension

    ROCM_HOME = cpp_extension._find_rocm_home()
    if not ROCM_HOME:
        raise VerifyDynamoError(
            "ROCM was not found on the system, please set ROCM_HOME environment variable"
        )

    hipcc = os.path.join(ROCM_HOME, "bin", "hipcc")
    hip_version_str = (
        subprocess.check_output([hipcc, "--version"])
        .strip()
        .decode(*cpp_extension.SUBPROCESS_DECODE_ARGS)
    )
    hip_version = re.search(r"HIP version: (\d+[.]\d+)", hip_version_str)

    if hip_version is None:
        raise VerifyDynamoError("HIP version not found in `hipcc --version` output")

    hip_str_version = hip_version.group(1)

    return TorchVersion(hip_str_version)
