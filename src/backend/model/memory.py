from dataclasses import dataclass


@dataclass
class Memory:
    total: int
    available: int
    used: int
    percent: float

    swap_total: int
    swap_used: int
    swap_free: int
    swap_percent: float

    @property
    def total_gb(self) -> float:
        return self.total / (1024**3)

    @property
    def used_gb(self) -> float:
        return self.used / (1024**3)

    @property
    def available_gb(self) -> float:
        return self.available / (1024**3)

    @property
    def available_percent(self) -> float:
        if self.total <= 0:
            return 0.0

        return (self.available / self.total) * 100

    @property
    def swap_total_gb(self) -> float:
        return self.swap_total / (1024**3)

    @property
    def swap_used_gb(self) -> float:
        return self.swap_used / (1024**3)

    @property
    def swap_active(self) -> bool:
        return self.swap_used > 0

    @property
    def is_under_pressure(self) -> bool:
        return self.percent >= 80

    @property
    def is_critical(self) -> bool:
        return self.percent >= 95
