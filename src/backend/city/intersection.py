from dataclasses import dataclass, field


@dataclass
class Intersection:

    id: str

    position: tuple[float, float, float] = (0.0, 0.0, 0.0)

    road_ids: list[str] = field(default_factory=list)

    traffic: float = 0.0

    metadata: dict = field(default_factory=dict)

    @property
    def x(self):
        return self.position[0]

    @property
    def y(self):
        return self.position[1]

    @property
    def z(self):
        return self.position[2]

    def add_road(self, road_id):

        if road_id not in self.road_ids:
            self.road_ids.append(road_id)

    def set_traffic(self, value):

        self.traffic = max(0.0, min(1.0, value))
