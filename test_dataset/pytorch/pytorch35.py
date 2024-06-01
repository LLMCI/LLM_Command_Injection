def test_kineto_profiler_with_environment_variable(self):
        script = """
import torch
import torch.nn as nn
from torch.profiler import supported_activities, profile
from torch.autograd.profiler import KinetoStepTracker

class SimpleNet(nn.Module):
    def __init__(self):
        super().__init__()
        self.fc1 = nn.Linear(10, 5)
        self.fc2 = nn.Linear(5, 2)

    def forward(self, x):
        return self.fc2(self.fc1(x))


def payload(use_cuda=False):
    x = torch.randn(10, 10)
    if use_cuda:
        x = x.cuda()
    y = torch.randn(10, 10)
    if use_cuda:
        y = y.cuda()
    z = torch.mm(x, y)
    z = z + y
    if use_cuda:
        z = z.cpu()

niters = 8
use_cuda = torch.profiler.ProfilerActivity.CUDA in supported_activities()
net = SimpleNet()
opt = torch.optim.SGD(net.parameters(), lr=0.01)
opt.zero_grad()
inputs = torch.rand(10)

with profile(activities=supported_activities()):
    payload(use_cuda=use_cuda)

initial_step = KinetoStepTracker.current_step()

def run_batch():
    out = net(inputs)
    loss = torch.nn.functional.cross_entropy(out, torch.rand(2))
    loss.backward()
    opt.step()

for _ in range(niters):
    run_batch()

with profile(
    activities=supported_activities(),
    schedule=torch.profiler.schedule(
        wait=1,
        warmup=1,
        active=2),
) as p:
    for _ in range(niters):
        run_batch()
        p.step()
assert KinetoStepTracker.current_step() == initial_step + 2 * niters
"""
        try:
            subprocess.check_output(
                [sys.executable, '-W', 'all', '-c', script],
                cwd=os.path.dirname(os.path.realpath(__file__))
            )
        except subprocess.CalledProcessError as e:
            if e.returncode != 0:
                self.assertTrue(False, "Kineto is not working properly with the Dynolog environment variable")

