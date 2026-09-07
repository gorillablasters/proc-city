import psutil
import socket
import platform

from ..model.hardware import Hardware


def collect_hardware() -> Hardware:
    hostname = socket.gethostname()
    platform_system = platform.system()
    architecture = psutil.cpu_info().arch if hasattr(psutil, "cpu_info") else "Unknown"
    cpu_name = psutil.cpu_info().brand if hasattr(psutil, "cpu_info") else "Unknown"
    total_memory = psutil.virtual_memory().total
    gpu_names = (
        [gpu.name for gpu in psutil.gpu_info()] if hasattr(psutil, "gpu_info") else []
    )
    hardware = Hardware(
        hostname=hostname,
        platform=platform_system,
        architecture=architecture,
        cpu_name=cpu_name,
        total_memory=total_memory,
        gpu_names=gpu_names,
    )
    return hardware
