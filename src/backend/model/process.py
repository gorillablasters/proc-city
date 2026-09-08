from dataclasses import dataclass
import time
from typing import Optional


@dataclass
class Process:
    pid: int
    parent_pid: Optional[int]
    name: str
    executable: Optional[str]
    username: Optional[str]
    status: str
    create_time: float
    cpu_percent: float
    cpu_user_time: float
    cpu_system_time: float
    threads: int
    memory_rss: int
    memory_vms: int
    memory_percent: float
    read_count: int
    write_count: int
    read_bytes: int
    write_bytes: int
    nice: Optional[int]
    connections: int

    @property
    def stable_id(self) -> str:
        return f"process:{self.pid}:{self.create_time}"

    @property
    def has_parent(self) -> bool:
        return self.parent_pid is not None and self.parent_pid > 0

    @property
    def runtime(self) -> float:
        """Process runtime in seconds."""
        return max(0.0, time.time() - self.create_time)

    @property
    def runtime_minutes(self) -> float:
        return self.runtime / 60

    @property
    def runtime_hours(self) -> float:
        return self.runtime / 3600

    @property
    def is_running(self) -> bool:
        return self.status == "running"

    @property
    def is_sleeping(self) -> bool:
        return self.status in ("sleeping", "idle")

    @property
    def is_stopped(self) -> bool:
        return self.status in ("stopped", "tracing-stop")

    @property
    def is_zombie(self) -> bool:
        return self.status == "zombie"

    @property
    def total_cpu_time(self) -> float:
        return self.cpu_user_time + self.cpu_system_time

    @property
    def cpu_active(self) -> bool:
        return self.cpu_percent > 0

    @property
    def memory_gb(self) -> float:
        return self.memory_rss / (1024**3)

    @property
    def virtual_memory_gb(self) -> float:
        return self.memory_vms / (1024**3)

    @property
    def total_io_bytes(self) -> int:
        return self.read_bytes + self.write_bytes

    @property
    def total_io_operations(self) -> int:
        return self.read_count + self.write_count

    @property
    def has_io_activity(self) -> bool:
        return self.total_io_bytes > 0 or self.total_io_operations > 0

    @property
    def is_networked(self) -> bool:
        return self.connections > 0

    @property
    def is_default_priority(self) -> bool:
        return self.nice == 0 if self.nice is not None else False
