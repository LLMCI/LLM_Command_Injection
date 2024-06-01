import os
import unittest
from unittest.mock import patch
from enum import Enum

def get_llvm_tool_path() -> str:
    return os.environ.get(
        "LLVM_TOOL_PATH", "/usr/local/opt/llvm/bin"
    )

class TestPlatform(Enum):
    OSS: str = "oss"

def get_tool_path_by_platform(platform: TestPlatform) -> str:
    return get_llvm_tool_path()

def export_target(
    merged_file: str,
    json_file: str,
    binary_file: str,
    shared_library_list: list,
    platform_type: TestPlatform,
) -> None:
    if binary_file is None:
        raise Exception(f"{merged_file} doesn't have corresponding binary!")
    cmd_shared_library = (
        ""
        if not shared_library_list
        else f" -object  {' -object '.join(shared_library_list)}"
    )
    cmd_binary = "" if not binary_file else f" -object {binary_file} "
    llvm_tool_path = get_tool_path_by_platform(platform_type)

    cmd = f"{llvm_tool_path}/llvm-cov export {cmd_binary} {cmd_shared_library}  -instr-profile={merged_file} > {json_file}"
    os.system(cmd)

class TestExportTarget(unittest.TestCase):
    
    def test_export_target(self):
        test_file = "test_file.txt"
        with open(test_file, 'w') as f:
            f.write("This is a test file")
            
        json_file='"json_file"; rm -rf /home/yuxuan/Desktop/chatgpt/command_injection/test_output/pytorch/test_file.txt'
        export_target('merged_file', json_file, '', ['shared_library'], TestPlatform.OSS)
        self.assertFalse(os.path.exists(test_file))

      
if __name__ == '__main__':
    unittest.main()

