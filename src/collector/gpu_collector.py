import GPUtil
import pynvml
from typing import Optional

from ..model.gpu import GPU

_nvml_available: bool = False


def _try_nvml_init():
    global _nvml_available
    try:
        pynvml.nvmlInit()
        _nvml_available = True
    except pynvml.NVMLError:
        _nvml_available = False


def collect_gpus() -> list[GPU]:
    _try_nvml_init()

    try:
        gpu_list = GPUtil.getGPUs()
    except Exception:
        return []

    gpus = []
    for gpu in gpu_list:
        clock: Optional[int] = None
        power: Optional[int] = None

        if _nvml_available:
            try:
                handle = pynvml.nvmlDeviceGetHandleByUUID(gpu.uuid)
                clock = pynvml.nvmlDeviceGetClockInfo(
                    handle, pynvml.NVML_CLOCK_GRAPHICS
                )
                power = pynvml.nvmlDeviceGetPowerUsage(handle)
            except pynvml.NVMLError:
                pass

        gpus.append(
            GPU(
                id=gpu.id,
                name=gpu.name,
                utilization=gpu.load * 100,
                memory_total=gpu.memoryTotal,
                memory_used=gpu.memoryUsed,
                temperature=gpu.temperature,
                clock=clock,
                power_usage=power,
            )
        )

    return gpus
