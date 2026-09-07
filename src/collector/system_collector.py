from ..model.system import System
from .hardware_collector import collect_hardware
from .cpu_collector import collect_cpu
from .memory_collector import collect_memory
from .gpu_collector import collect_gpus
from .process_collector import collect_processes
from .network_collector import collect_network
from .storage_collector import collect_storage
from .sensor_collector import collect_sensors


def collect_system() -> System:
    hardware = collect_hardware()
    cpu = collect_cpu()
    memory = collect_memory()
    gpus = collect_gpus()
    processes = collect_processes()
    network = collect_network()
    storage = collect_storage()
    sensors = collect_sensors()
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
