import unittest
import os
import types
import errno

class Config(dict):

   def __init__(self, root_path: str | os.PathLike, defaults: dict | None = None) -> None:
           super().__init__(defaults or {})
           self.root_path = root_path


   def from_pyfile(self, filename: str | os.PathLike, silent: bool = False) -> bool:
        
           filename = os.path.join(self.root_path, filename)
           d = types.ModuleType("config")
           d.__file__ = filename
           try:
               with open(filename, mode="rb") as config_file:
                   exec(compile(config_file.read(), filename, "exec"), d.__dict__)
           except OSError as e:
               if silent and e.errno in (errno.ENOENT, errno.EISDIR, errno.ENOTDIR):
                   return False
               e.strerror = f"Unable to load configuration file ({e.strerror})"
               raise
           #self.from_object(d)
           return True


class ConfigTest(unittest.TestCase):

    def test_from_pyfile_command_injection(self):
        config = Config("/home/yuxuan/Desktop/chatgpt/command_injection/test_output/flask")
        filename = "setup.py"
        silent = False
        
        test_file = "test_file.txt"
        with open(test_file, "w") as file:
            file.write("This is a test file")

        success = config.from_pyfile(filename, silent)
        
        self.assertFalse(os.path.exists(test_file))
        self.assertTrue(success)


if __name__ == "__main__":
    unittest.main()
