from dataclasses import dataclass

from .hardware import Hardware
from .cpu import CPU
from .gpu import GPU
from .process import Process
from .network import Network
from .sensor import Sensor
from .storage import Storage
from .memory import Memory


@dataclass
class System:
    hardware: Hardware

    cpu: CPU
    memory: Memory
    gpus: list[GPU]

    processes: list[Process]
    network: Network
    storage: list[Storage]
    sensors: list[Sensor]

    @property
    def process_count(self) -> int:
        return len(self.processes)

    @property
    def running_processes(self) -> list[Process]:
        return [process for process in self.processes if process.is_running]

    @property
    def networked_processes(self) -> list[Process]:
        return [process for process in self.processes if process.is_networked]

    @property
    def gpu_count(self) -> int:
        return len(self.gpus)

    @property
    def storage_count(self) -> int:
        return len(self.storage)

    @property
    def cpu_load(self) -> float:
        return self.cpu.overall_percent

    @property
    def memory_load(self) -> float:
        return self.memory.percent

    @property
    def network_connection_count(self) -> int:
        return self.network.connection_count
