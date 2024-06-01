def nvcc_exist(nvcc_path: str = "nvcc") -> bool:
    if nvcc_path is None:
        return False
    import subprocess

    res = subprocess.call(
        ["which", nvcc_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
    )
    return res == 0
    
    
