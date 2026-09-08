import GPUtil
import pynvml
from typing import Optional

from ..decorator import aliased, alias
from ..model.gpu import GPU


@aliased
class GPUCollector:
    def __init__(self):
        self._nvml_available = False
        self._try_nvml_init()

    def _try_nvml_init(self):
        try:
            pynvml.nvmlInit()
            self._nvml_available = True
        except pynvml.NVMLError:
            self._nvml_available = False

    @alias("collect")
    def collect_gpus(self) -> list[GPU]:

        try:
            gpu_list = GPUtil.getGPUs()
        except Exception:
            return []

        gpus = []
        for gpu in gpu_list:
            clock: Optional[int] = None
            power: Optional[int] = None

            if self._nvml_available:
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
