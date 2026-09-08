from dataclasses import dataclass, field


@dataclass
class CityBlock:

    id: str

    district: str

    position: tuple[float, float, float] = (0.0, 0.0, 0.0)

    size: tuple[float, float] = (32.0, 32.0)

    building_ids: list[str] = field(default_factory=list)

    intersection_ids: list[str] = field(default_factory=list)

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

    @property
    def width(self):
        return self.size[0]

    @property
    def depth(self):
        return self.size[1]

    def add_building(self, building_id):

        if building_id not in self.building_ids:
            self.building_ids.append(building_id)

    def remove_building(self, building_id):

        if building_id in self.building_ids:
            self.building_ids.remove(building_id)

    def add_intersection(self, intersection_id):

        if intersection_id not in self.intersection_ids:
            self.intersection_ids.append(intersection_id)
