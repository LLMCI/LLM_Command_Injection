class TestStatelessDeprecation(TestCase):
    def test_private_stateless_warns(self):
        script = """
import torch
import warnings

with warnings.catch_warnings(record=True) as w:
    from torch.nn.utils import _stateless

exit(len(w))
"""
        try:
            subprocess.check_output(
                [sys.executable, '-W', 'all', '-c', script],
                stderr=subprocess.STDOUT,
                # On Windows, opening the subprocess with the default CWD makes `import torch`
                # fail, so just set CWD to this script's directory
                cwd=os.path.dirname(os.path.realpath(__file__)),)
        except subprocess.CalledProcessError as e:
            self.assertEqual(e.returncode, 1)
        else:
            self.assertTrue(False, "No warning was raised.")

    def test_stateless_functional_call_warns(self):
        m = torch.nn.Linear(1, 1)
        params = dict(m.named_parameters())
        x = torch.randn(3, 1)
        with self.assertWarnsRegex(UserWarning, "Please use torch.func.functional_call"):
            stateless.functional_call(m, params, x)

class TestPythonOptimizeMode(TestCase):
    def test_runs_with_optimize_flag(self):
        script = "import torch; import torch._functorch.deprecated"
        try:
            subprocess.check_output(
                [sys.executable, "-OO", "-c", script],
                stderr=subprocess.STDOUT,
                # On Windows, opening the subprocess with the default CWD makes `import torch`
                # fail, so just set CWD to this script's directory
                cwd=os.path.dirname(os.path.realpath(__file__)),)
        except subprocess.CalledProcessError as e:
            self.assertFalse(e.returncode, "Import failed while running python in optimized mode")
