from ..decorator import aliased, alias
from ..model.system import System
from .hardware_collector import HardwareCollector
from .cpu_collector import CPUCollector
from .memory_collector import MemoryCollector
from .gpu_collector import GPUCollector
from .process_collector import ProcessCollector
from .network_collector import NetworkCollector
from .storage_collector import StorageCollector
from .sensor_collector import SensorCollector


@aliased
class SystemCollector:
    def __init__(self):
        self.hardware_collector = HardwareCollector()
        self.cpu_collector = CPUCollector()
        self.memory_collector = MemoryCollector()
        self.gpu_collector = GPUCollector()
        self.process_collector = ProcessCollector()
        self.network_collector = NetworkCollector()
        self.storage_collector = StorageCollector()
        self.sensor_collector = SensorCollector()

    @alias("collect")
    def collect_system(self) -> System:
        hardware = self.hardware_collector.collect()
        cpu = self.cpu_collector.collect()
        memory = self.memory_collector.collect()
        gpus = self.gpu_collector.collect()
        processes = self.process_collector.collect()
        network = self.network_collector.collect()
        storage = self.storage_collector.collect()
        sensors = self.sensor_collector.collect()
        return System(
            hardware=hardware,
            cpu=cpu,
            memory=memory,
            gpus=gpus,
            processes=processes,
            network=network,
            storage=storage,
            sensors=sensors,
        )
