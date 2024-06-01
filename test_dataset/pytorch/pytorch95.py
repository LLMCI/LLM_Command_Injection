import tempfile

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
    assert num == 4, "Failed to launch multiple instances for inference"
