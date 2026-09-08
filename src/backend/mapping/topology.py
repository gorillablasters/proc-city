from ..city import CityBlock, Intersection, Road


class CityTopologyBuilder:

    BLOCK_SIZE = 32.0
    STREET_SIZE = 8.0

    BLOCKS_PER_DISTRICT = 3

    DISTRICT_SPACING = 140.0

    DISTRICTS = {
        "infrastructure": (0, 0),
        "industrial": (140, 0),
        "network": (280, 0),
        "commercial": (0, 140),
        "warehouse": (140, 140),
        "temporary": (280, 140),
        "generic": (0, 280),
    }

    def build(self, city):
        self._create_blocks(city)
        self._create_intersections(city)
        self._create_roads(city)

        return city

    def _create_blocks(self, city):

        spacing = self.BLOCK_SIZE + self.STREET_SIZE

        for district, origin in self.DISTRICTS.items():

            origin_x, origin_y = origin

            for row in range(self.BLOCKS_PER_DISTRICT):

                for column in range(self.BLOCKS_PER_DISTRICT):

                    x = origin_x + column * spacing
                    y = origin_y + row * spacing

                    block_id = f"block:{district}:{row}:{column}"

                    block = CityBlock(
                        id=block_id,
                        district=district,
                        position=(x, y, 0.0),
                        size=(
                            self.BLOCK_SIZE,
                            self.BLOCK_SIZE,
                        ),
                    )

                    city.add_block(block)

    def _create_intersections(self, city):

        intersection_by_position = {}

        half_block = self.BLOCK_SIZE / 2
        half_street = self.STREET_SIZE / 2

        for block in city.blocks.values():

            x, y, _ = block.position

            half = half_block + half_street

            positions = [
                (x - half, y - half, 0.0),
                (x + half, y - half, 0.0),
                (x - half, y + half, 0.0),
                (x + half, y + half, 0.0),
            ]

            for position in positions:

                key = (
                    round(position[0], 3),
                    round(position[1], 3),
                )

                if key not in intersection_by_position:

                    intersection_id = (
                        f"intersection:" f"{len(intersection_by_position)}"
                    )

                    intersection = Intersection(
                        id=intersection_id,
                        position=position,
                    )

                    city.add_intersection(intersection)

                    intersection_by_position[key] = intersection

                intersection = intersection_by_position[key]

                block.add_intersection(intersection.id)

    def _create_roads(self, city):

        intersections = list(city.intersections.values())

        tolerance = 0.01

        for source in intersections:

            for destination in intersections:

                if source.id == destination.id:
                    continue

                sx, sy, _ = source.position
                dx, dy, _ = destination.position

                same_x = abs(sx - dx) < tolerance
                same_y = abs(sy - dy) < tolerance

                distance = abs(dx - sx) + abs(dy - sy)

                if not (same_x or same_y):
                    continue

                if distance > (self.BLOCK_SIZE + self.STREET_SIZE + tolerance):
                    continue

                road_id = (
                    f"road:"
                    f"{min(source.id, destination.id)}:"
                    f"{max(source.id, destination.id)}"
                )

                if road_id in city.roads:
                    continue

                road = Road(
                    id=road_id,
                    source_id=source.id,
                    destination_id=destination.id,
                    traffic=0.0,
                    metadata={
                        "physical": True,
                        "road_type": "street",
                    },
                )

                city.add_road(road)

                source.add_road(road.id)
                destination.add_road(road.id)
