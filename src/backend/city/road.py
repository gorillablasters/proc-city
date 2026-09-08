from dataclasses import dataclass, field


@dataclass
class Road:

    id: str

    source_id: str

    destination_id: str

    traffic: float = 0.0

    active: bool = True

    metadata: dict = field(default_factory=dict)

    @property
    def endpoints(self) -> tuple[str, str]:
        return (self.source_id, self.destination_id)

    def set_traffic(self, value: float):
        self.traffic = max(0.0, min(1.0, value))
