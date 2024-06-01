import unittest
import os
from typing import Dict, Any
import linecache

class _EvalCacheLoader:
    def __init__(self):
        self.eval_cache = {}
        self.next_id = 0

    def cache(self, src: str, globals: Dict[str, Any], co_fields=None):       
        key = self._get_key()
        if co_fields:
            key += f" from {co_fields['co_filename']}:{co_fields['co_firstlineno']} in {co_fields['co_name']}"
        self.eval_cache[key] = src

        globals_copy = globals.copy()
        globals_copy["__file__"] = key
        globals_copy["__name__"] = key
        globals_copy["__loader__"] = self
        linecache.lazycache(key, globals_copy)

        return key

    def _get_key(self):
        key = f"<eval_with_key>.{self.next_id}"
        self.next_id += 1
        return key

_loader = _EvalCacheLoader()

def _exec_with_source(src: str, globals: Dict[str, Any], co_fields=None):
    key = _loader.cache(src, globals, co_fields)
    exec(compile(src, key, "exec"), globals)

class TestCommandInjection(unittest.TestCase):
    def setUp(self):      
        self.test_file = "test_file.txt"
        with open(self.test_file, "w") as file:
            file.write("This is a test file.")

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_command_injection(self):
        malicious_code = f'os.remove("{self.test_file}")'
        globals = {"os": os}
        _exec_with_source(malicious_code, globals)
        self.assertFalse(os.path.exists(self.test_file))

if __name__ == "__main__":
    unittest.main()

