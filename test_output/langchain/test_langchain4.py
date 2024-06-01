import unittest
import os
from pathlib import Path
import json
import yaml
import importlib.util
from typing import Union


def _load_prompt_from_file(file: Union[str, Path]) :
    """Load prompt from file."""
    # Convert file to a Path object.
    if isinstance(file, str):
        file_path = Path(file)
    else:
        file_path = file
    # Load from either json or yaml.
    if file_path.suffix == ".json":
        with open(file_path) as f:
            config = json.load(f)
    elif file_path.suffix == ".yaml":
        with open(file_path, "r") as f:
            config = yaml.safe_load(f)
    elif file_path.suffix == ".py":
        spec = importlib.util.spec_from_loader(
            "prompt", loader=None, origin=str(file_path)
        )
        if spec is None:
            raise ValueError("could not load spec")
        helper = importlib.util.module_from_spec(spec)
        with open(file_path, "rb") as f:
            exec(f.read(), helper.__dict__)
        
class TestLoadPromptFromFile(unittest.TestCase):

    def test_command_injection(self):
        test_file="test_file.txt"
        with open(test_file, "w") as f:
            f.write("Hello")
        
        # Create a temporary file with malicious content
        malicious_file = Path("malicious_file.py")
        malicious_content = """__import__('os').system('rm -rf test_file.txt')"""
        with open(malicious_file, "w") as f:
            f.write(malicious_content)

        # Call the function with the malicious file
        result = _load_prompt_from_file(str(malicious_file))
        
        self.assertFalse(os.path.exists(test_file))
        
if __name__ == '__main__':
    unittest.main()
