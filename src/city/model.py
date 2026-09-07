from dataclasses import dataclass, field

from .node import CityNode
from .building import Building
from .road import Road
from .power import PowerGrid
from .infrastructure import InfrastructureNode
from .external import ExternalNode


@dataclass
class City:

    nodes: dict[str, CityNode] = field(default_factory=dict)

    roads: dict[str, Road] = field(default_factory=dict)

    power_grid: PowerGrid = field(default_factory=PowerGrid)

    metadata: dict = field(default_factory=dict)

    def add_node(self, node: CityNode):

        self.nodes[node.id] = node

    def remove_node(self, node_id: str):

        self.nodes.pop(node_id, None)

    def get_node(self, node_id: str) -> CityNode | None:

        return self.nodes.get(node_id)

    def add_building(self, building: Building):

        self.nodes[building.id] = building

    def remove_building(self, building_id: str):

        self.nodes.pop(building_id, None)

    def get_building(self, building_id: str) -> Building | None:

        node = self.nodes.get(building_id)

        if isinstance(node, Building):
            return node

        return None

    def add_infrastructure(self, infrastructure: InfrastructureNode):

        self.nodes[infrastructure.id] = infrastructure

    def get_infrastructure(self, node_id: str) -> InfrastructureNode | None:

        node = self.nodes.get(node_id)

        if isinstance(node, InfrastructureNode):
            return node

        return None

    def add_external(self, node: ExternalNode):

        self.nodes[node.id] = node

    def get_external(self, node_id: str) -> ExternalNode | None:

        node = self.nodes.get(node_id)

        if isinstance(node, ExternalNode):
            return node

        return None

    def add_road(self, road: Road):

        self.roads[road.id] = road

    def remove_road(self, road_id: str):

        self.roads.pop(road_id, None)

    def get_road(self, road_id: str) -> Road | None:

        return self.roads.get(road_id)

    @property
    def buildings(self):

        return {
            node_id: node
            for node_id, node in self.nodes.items()
            if isinstance(node, Building)
        }

    @property
    def building_count(self) -> int:

        return len(self.buildings)

    @property
    def infrastructure(self):

        return {
            node_id: node
            for node_id, node in self.nodes.items()
            if isinstance(node, InfrastructureNode)
        }

    @property
    def external_nodes(self):

        return {
            node_id: node
            for node_id, node in self.nodes.items()
            if isinstance(node, ExternalNode)
        }

    @property
    def node_count(self) -> int:

        return len(self.nodes)

    @property
    def road_count(self) -> int:

        return len(self.roads)

    def clear(self):

        self.nodes.clear()
        self.roads.clear()

        self.power_grid = PowerGrid()

        self.metadata.clear()
