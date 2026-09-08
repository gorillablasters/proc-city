from dataclasses import dataclass

from .node import CityNode


@dataclass
class Building(CityNode):

    building_type: str = "generic"

    process_id: str | None = None

    def __post_init__(self):

        self.node_type = "building"
