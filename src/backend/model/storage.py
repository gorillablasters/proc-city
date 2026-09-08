from dataclasses import dataclass
from typing import Optional


@dataclass
class Storage:
    device: str

    mountpoint: Optional[str]

    fstype: Optional[str]

    total: int
    used: int
    free: int
    percent: float

    read_count: int
    write_count: int

    read_bytes: int
    write_bytes: int

    @property
    def total_gb(self) -> float:
        return self.total / (1024**3)

    @property
    def used_gb(self) -> float:
        return self.used / (1024**3)

    @property
    def free_gb(self) -> float:
        return self.free / (1024**3)

    @property
    def total_io_bytes(self) -> int:
        return self.read_bytes + self.write_bytes

    @property
    def total_io_operations(self) -> int:
        return self.read_count + self.write_count

    @property
    def is_nearly_full(self) -> bool:
        return self.percent >= 80

    @property
    def is_full(self) -> bool:
        return self.percent >= 95
