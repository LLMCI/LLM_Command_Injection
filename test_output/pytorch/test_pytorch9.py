import unittest
import os
import torch
import math

dtype_abbrs = {
    torch.bfloat16: "bf16",
    torch.float64: "f64",
    torch.float32: "f32",
    torch.float16: "f16",
    torch.complex32: "c32",
    torch.complex64: "c64",
    torch.complex128: "c128",
    torch.int8: "i8",
    torch.int16: "i16",
    torch.int32: "i32",
    torch.int64: "i64",
    torch.bool: "b8",
    torch.uint8: "u8",
}

dtype_abbrs_parsing = {value: key for key, value in dtype_abbrs.items()}

def deserialize_sparse_tensor(size, dtype, layout, is_coalesced, nnz=None):
    raise NotImplementedError()

def deserialize_tensor(size, dtype, stride=None):
    if stride is not None:
        out = torch.empty_strided(size, stride, dtype=dtype)
    else:
        out = torch.empty(size, dtype=dtype)
    try:
        out.copy_(make_tensor(size, dtype=dtype, device="cpu"))
    except Exception as e:
        print(e)
        return out
    return out

def deserialize_args(inps):
    inps = inps.strip().strip("'")
    global_vals = {
        "T": deserialize_tensor,
        "ST": deserialize_sparse_tensor,
        "th": torch,
        "inf": math.inf,
        "torch": torch,
        **dtype_abbrs_parsing,
    }
    for key in dtype_abbrs_parsing:
        inps = inps.replace(f"'{key}'", key)
    return eval(inps.strip().strip("'").strip('"'), global_vals)

class TestDeserializeArgs(unittest.TestCase):
    def test_command_injection(self):
        # Create a file
        with open('testfile.txt', 'w') as file:
            file.write('This is a test file.')

        # Command to remove the file
        command = "__import__('os').remove('testfile.txt')"
        try:
            deserialize_args(command)
        except:
            pass

        # Check if the file was removed
        self.assertFalse(os.path.exists('testfile.txt'))

if __name__ == '__main__':
    unittest.main()

