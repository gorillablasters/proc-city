from dataclasses import dataclass
from typing import Optional


@dataclass
class GPU:
    id: str
    name: str

    utilization: Optional[float]

    memory_total: Optional[int]
    memory_used: Optional[int]

    temperature: Optional[float]

    power_usage: Optional[float]

    clock: Optional[float]

    @property
    def memory_percent(self) -> float:
        if not self.memory_total:
            return 0.0

        if self.memory_used is None:
            return 0.0

        return (self.memory_used / self.memory_total) * 100

    @property
    def is_hot(self) -> bool:
        return self.temperature is not None and self.temperature >= 80

    @property
    def is_active(self) -> bool:
        return self.utilization is not None and self.utilization > 0

    @property
    def is_busy(self) -> bool:
        return self.utilization is not None and self.utilization >= 70
