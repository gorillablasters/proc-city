import math


class CityLayout:

    DISTRICTS = {
        "infrastructure": (0.0, 0.0),
        "industrial": (100.0, 0.0),
        "network": (200.0, 0.0),
        "commercial": (0.0, 100.0),
        "warehouse": (100.0, 100.0),
        "temporary": (200.0, 100.0),
        "generic": (0.0, 200.0),
    }

    def __init__(self, spacing=10.0, row_spacing=10.0):
        self.spacing = spacing
        self.row_spacing = row_spacing

    def layout(self, city):

        buildings_by_type = {}

        for building in city.buildings.values():

            building_type = building.building_type

            buildings_by_type.setdefault(building_type, []).append(building)

        for building_type, buildings in buildings_by_type.items():

            self._layout_district(buildings, building_type)

    def _layout_district(self, buildings, building_type):

        origin = self.DISTRICTS.get(building_type, self.DISTRICTS["generic"])

        origin_x, origin_z = origin

        unplaced = [
            building for building in buildings if building.position == (0.0, 0.0, 0.0)
        ]

        if not unplaced:
            return

        occupied = {
            building.position
            for building in buildings
            if building.position != (0.0, 0.0, 0.0)
        }

        columns = max(1, math.ceil(math.sqrt(len(buildings))))

        for building in unplaced:

            index = 0

            while True:

                row = index // columns
                column = index % columns

                position = (
                    origin_x + column * self.spacing,
                    0.0,
                    origin_z + row * self.row_spacing,
                )

                if position not in occupied:
                    break

                index += 1

            building.position = position

            occupied.add(position)
