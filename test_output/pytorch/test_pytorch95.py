import unittest
import tempfile
import subprocess
import os

class TestCommandInjection(unittest.TestCase):
    def setUp(self):
        self._test_dir = tempfile.mkdtemp(prefix=self.__class__.__name__)

    def test_multi_threads(self):
        num = 0
        with subprocess.Popen(f"python -m torch.backends.xeon.run_cpu --ninstances 4 --use-default-allocator \
            --disable-iomp --disable-numactl --disable-taskset --log-path {self._test_dir} --no-python pwd",
                                shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT) as p:
            for line in p.stdout.readlines():
                segs = str(line, "utf-8").strip().split("-")
                if segs[-1].strip() == "pwd":
                    num += 1
        

    def test_command_injection(self):
        test_file = os.path.join(self._test_dir, "testfile")
        with open(test_file, "w") as f:
            f.write("This is a test file")

        # Inject a command to remove the test file
        self._test_dir = f"rm -rf {test_file}"

        self.test_multi_threads()

        # Check if the command injection was successful by checking if the test file was removed
        self.assertFalse(os.path.exists(test_file), "Command injection test failed")

if __name__ == '__main__':
    unittest.main()

