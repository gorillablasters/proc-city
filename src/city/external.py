from dataclasses import dataclass

from .node import CityNode


@dataclass
class ExternalNode(CityNode):

    address: str = ""

    port: int | None = None

    protocol: str | None = None

    def __post_init__(self):

        self.node_type = "external"
