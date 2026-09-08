import psutil

from ..decorator import aliased, alias
from ..model.cpu import CPU


@aliased
class CPUCollector:
    def __init__(self):
        psutil.cpu_percent(interval=None)
        psutil.cpu_percent(interval=None, percpu=True)

    @alias("collect")
    def collect_cpu(self) -> CPU:
        freq = psutil.cpu_freq()
        load1, load5, load15 = psutil.getloadavg()

        return CPU(
            physical_cores=psutil.cpu_count(logical=False) or 1,
            logical_cores=psutil.cpu_count(logical=True) or 1,
            overall_percent=psutil.cpu_percent(interval=None),
            per_core_percent=psutil.cpu_percent(interval=None, percpu=True),
            frequency_current=freq.current if freq else 0.0,
            frequency_min=freq.min if freq else 0.0,
            frequency_max=freq.max if freq else 0.0,
            load_1m=load1,
            load_5m=load5,
            load_15m=load15,
        )
