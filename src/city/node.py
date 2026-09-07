from dataclasses import dataclass, field


@dataclass
class CityNode:

    id: str
    name: str

    node_type: str = "generic"

    position: tuple[float, float, float] = (0.0, 0.0, 0.0)

    activity: float = 0.0
    active: bool = True

    metadata: dict = field(default_factory=dict)

    source_id: str | None = None

    @property
    def x(self) -> float:
        return self.position[0]

    @property
    def y(self) -> float:
        return self.position[1]

    @property
    def z(self) -> float:
        return self.position[2]

    def set_activity(self, value: float):

        self.activity = max(0.0, min(1.0, value))
