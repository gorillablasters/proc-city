from dataclasses import dataclass


@dataclass
class ProcessTraits:

    cpu_intensive: bool = False
    memory_intensive: bool = False
    network_active: bool = False
    storage_active: bool = False

    long_running: bool = False
    short_lived: bool = False

    multi_threaded: bool = False
    parent_process: bool = False
    child_process: bool = False

    interactive: bool = False
    background: bool = False

    high_activity: bool = False

    @property
    def resource_intensive(self) -> bool:
        return (
            self.cpu_intensive
            or self.memory_intensive
            or self.storage_active
            or self.network_active
        )

    @property
    def infrastructure_like(self) -> bool:
        return self.background and self.long_running


class ProcessTraitAnalyzer:

    CPU_THRESHOLD = 20.0
    MEMORY_THRESHOLD = 5.0
    IO_THRESHOLD = 1024 * 1024
    THREAD_THRESHOLD = 4

    def analyze(self, process):

        traits = ProcessTraits()

        traits.cpu_intensive = process.cpu_percent >= self.CPU_THRESHOLD

        traits.memory_intensive = process.memory_percent >= self.MEMORY_THRESHOLD

        traits.network_active = process.connections > 0

        traits.storage_active = (
            process.read_bytes >= self.IO_THRESHOLD
            or process.write_bytes >= self.IO_THRESHOLD
        )

        traits.long_running = process.runtime_hours >= 1

        traits.short_lived = process.runtime_minutes < 5

        traits.multi_threaded = process.threads >= self.THREAD_THRESHOLD

        traits.parent_process = process.parent_pid is None

        traits.child_process = process.parent_pid is not None

        traits.background = process.status in {"sleeping", "idle"}

        traits.high_activity = (
            process.cpu_percent >= 50
            or process.connections > 5
            or process.read_bytes >= self.IO_THRESHOLD * 5
            or process.write_bytes >= self.IO_THRESHOLD * 5
        )

        return traits
