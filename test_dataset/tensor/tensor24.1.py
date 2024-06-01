import re
import subprocess


def get_nvcc_version(path):
    pattern = r"Cuda compilation tools, release \d+\.\d+, V(\d+\.\d+\.\d+)"
    for line in subprocess.check_output([path, "--version"]).splitlines():
        match = re.match(pattern, line.decode("ascii"))
        if match:
            return match.group(1)
    return None
    
    

