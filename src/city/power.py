from dataclasses import dataclass, field


@dataclass
class PowerGrid:

    load: float = 0.0

    activity: float = 0.0

    capacity: float = 1.0

    metadata: dict = field(default_factory=dict)

    @property
    def utilization(self) -> float:

        if self.capacity <= 0:
            return 0.0

        return self.load / self.capacity

    @property
    def overloaded(self) -> bool:
        return self.utilization >= 1.0

    def set_load(self, value: float):

        self.load = max(0.0, value)

        self.activity = min(1.0, self.utilization)
