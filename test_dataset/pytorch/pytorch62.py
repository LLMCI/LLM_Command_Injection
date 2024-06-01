def get_cuda_version():
    from torch.torch_version import TorchVersion
    from torch.utils import cpp_extension

    CUDA_HOME = cpp_extension._find_cuda_home()
    if not CUDA_HOME:
        raise VerifyDynamoError(cpp_extension.CUDA_NOT_FOUND_MESSAGE)

    nvcc = os.path.join(CUDA_HOME, "bin", "nvcc")
    cuda_version_str = (
        subprocess.check_output([nvcc, "--version"])
        .strip()
        .decode(*cpp_extension.SUBPROCESS_DECODE_ARGS)
    )
    cuda_version = re.search(r"release (\d+[.]\d+)", cuda_version_str)
    if cuda_version is None:
        raise VerifyDynamoError("CUDA version not found in `nvcc --version` output")

    cuda_str_version = cuda_version.group(1)
    return TorchVersion(cuda_str_version)



