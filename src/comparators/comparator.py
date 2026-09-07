from ..snapshot.changes import SystemUpdate

from .process_comparator import ProcessComparator
from .cpu_comparator import CPUComparator
from .memory_comparator import MemoryComparator
from .network_comparator import NetworkComparator
from .storage_comparator import StorageComparator
from .gpu_comparator import GPUComparator
from .sensor_comparator import SensorComparator


class SnapshotComparator:

    def __init__(self):

        self.processes = ProcessComparator()
        self.cpu = CPUComparator()
        self.memory = MemoryComparator()
        self.network = NetworkComparator()
        self.storage = StorageComparator()
        self.gpu = GPUComparator()
        self.sensors = SensorComparator()

    def compare(self, previous, current):

        process_created, process_removed, process_changed = self.processes.compare(
            previous.system.processes, current.system.processes
        )

        cpu_changed = self.cpu.compare(previous.system.cpu, current.system.cpu)

        memory_changed = self.memory.compare(
            previous.system.memory, current.system.memory
        )

        network_created, network_removed, network_changed = self.network.compare(
            previous.system.network, current.system.network
        )

        storage_created, storage_removed, storage_changed = self.storage.compare(
            previous.system.storage, current.system.storage
        )

        gpu_created, gpu_removed, gpu_changed = self.gpu.compare(
            previous.system.gpus, current.system.gpus
        )

        sensor_created, sensor_removed, sensor_changed = self.sensors.compare(
            previous.system.sensors, current.system.sensors
        )

        return SystemUpdate(
            process_created=process_created,
            process_removed=process_removed,
            process_changed=process_changed,
            cpu_changed=cpu_changed,
            memory_changed=memory_changed,
            network_created=network_created,
            network_removed=network_removed,
            network_changed=network_changed,
            storage_created=storage_created,
            storage_removed=storage_removed,
            storage_changed=storage_changed,
            gpu_created=gpu_created,
            gpu_removed=gpu_removed,
            gpu_changed=gpu_changed,
            sensor_created=sensor_created,
            sensor_removed=sensor_removed,
            sensor_changed=sensor_changed,
        )
