from dataclasses import dataclass
from typing import Optional


@dataclass
class CPU:
    physical_cores: int
    logical_cores: int

    overall_percent: float
    per_core_percent: list[float]

    frequency_current: float
    frequency_min: float
    frequency_max: float

    load_1m: Optional[float]
    load_5m: Optional[float]
    load_15m: Optional[float]

    @property
    def core_utilization_average(self) -> float:
        if not self.per_core_percent:
            return 0.0

        return sum(self.per_core_percent) / len(self.per_core_percent)

    @property
    def busiest_core(self) -> float:
        if not self.per_core_percent:
            return 0.0

        return max(self.per_core_percent)

    @property
    def idle_percent(self) -> float:
        return max(0.0, 100.0 - self.overall_percent)

    @property
    def frequency_range(self) -> float:
        return max(0.0, self.frequency_max - self.frequency_min)

    @property
    def frequency_utilization(self) -> float:
        if self.frequency_max <= 0:
            return 0.0

        return self.frequency_current / self.frequency_max

    @property
    def is_active(self) -> bool:
        return self.overall_percent > 0

    @property
    def is_busy(self) -> bool:
        return self.overall_percent >= 70

    @property
    def is_heavily_loaded(self) -> bool:
        return self.overall_percent >= 90
