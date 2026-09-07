from dataclasses import dataclass, field

from .node import CityNode


@dataclass
class InfrastructureNode(CityNode):

    infrastructure_type: str = "generic"

    capacity: float = 1.0
    utilization: float = 0.0

    metadata: dict = field(default_factory=dict)

    def __post_init__(self):

        self.node_type = "infrastructure"

    def set_utilization(self, value: float):

        self.utilization = max(0.0, min(1.0, value))

        self.set_activity(self.utilization)

    @property
    def overloaded(self) -> bool:

        return self.utilization >= 1.0
