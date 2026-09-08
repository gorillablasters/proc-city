from dataclasses import dataclass
from typing import Optional


@dataclass
class Hardware:
    hostname: str
    platform: str
    architecture: str

    cpu_name: Optional[str]

    total_memory: int

    gpu_names: list[str]

    @property
    def memory_gb(self) -> float:
        return self.total_memory / (1024**3)

    @property
    def gpu_count(self) -> int:
        return len(self.gpu_names)
