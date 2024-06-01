import pickle
import subprocess
import time
import uuid
import atexit
import shutil
import enum
import os 
import dataclasses
from torch.utils.benchmark.utils.common import _make_temp_dir
from typing import List, Optional, TYPE_CHECKING, Union, Tuple
if TYPE_CHECKING:
    from torch.utils.benchmark.utils.timer import Language
else:
    from torch.utils.benchmark import Language


_TEMPDIR: Optional[str] = None
PopenType = subprocess.Popen

def get_temp_dir() -> str:
    global _TEMPDIR
    if _TEMPDIR is None:
        _TEMPDIR = _make_temp_dir(
            prefix="instruction_count_microbenchmarks", gc_dev_shm=True
        )
        atexit.register(shutil.rmtree, path=_TEMPDIR)
    return _TEMPDIR

Label = Tuple[str, ...]

class RuntimeMode(enum.Enum):
    EAGER = "Eager"
    JIT = "TorchScript"
    EXPLICIT = ""


class AutogradMode(enum.Enum):
    FORWARD = "Forward"
    FORWARD_BACKWARD = "Forward + Backward"
    EXPLICIT = ""


@dataclasses.dataclass(frozen=True)
class AutoLabels:
    """Labels for a TimerArgs instance which are inferred during unpacking."""

    runtime: RuntimeMode
    autograd: AutogradMode
    language: Language

class WorkerTimerArgs:
    stmt: str
    setup: str = "pass"
    global_setup: str = ""
    num_threads: int = 1
    language: Language = Language.PYTHON

WORKER_PATH = os.path.abspath(__file__)
_ENV = "MKL_THREADING_LAYER=GNU"
_PYTHON = "python"
SHELL = "/bin/bash"

class WorkOrder:
    label: Label
    autolabels: AutoLabels
    timer_args: WorkerTimerArgs
    source_cmd: Optional[str] = None
    timeout: Optional[float] = None
    retries: int = 0


class _BenchmarkProcess:
    _work_order: WorkOrder
    _cpu_list: Optional[str]
    _proc: PopenType
    _communication_file: str
       

    def __init__(self, work_order: WorkOrder, cpu_list: Optional[str]) -> None:
        self._communication_file = os.path.join(get_temp_dir(), f"{uuid.uuid4()}.pkl")
        self._proc = subprocess.Popen(
            self.cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            shell=True,
            executable=SHELL,
        )

    @property
    def cmd(self) -> str:
        cmd: List[str] = []
        if self._work_order.source_cmd is not None:
            cmd.extend([self._work_order.source_cmd, "&&"])

        cmd.append(_ENV)

        if self._cpu_list is not None:
            cmd.extend(
                [
                    f"GOMP_CPU_AFFINITY={self._cpu_list}",
                    "taskset",
                    "--cpu-list",
                    self._cpu_list,
                ]
            )

        cmd.extend(
            [
                _PYTHON,
                WORKER_PATH,
                "--communication-file",
                self._communication_file,
            ]
        )
        return " ".join(cmd)
