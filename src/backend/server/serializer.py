from ..city import City, Building, InfrastructureNode, ExternalNode


class CitySerializer:

    def serialize(self, city: City) -> dict:
        return {
            "version": "1.0",
            "city": self._serialize_city(city),
            "blocks": [self._serialize_block(block) for block in city.blocks.values()],
            "intersections": [
                self._serialize_intersection(intersection)
                for intersection in city.intersections.values()
            ],
            "roads": [self._serialize_road(road) for road in city.roads.values()],
            "nodes": [self._serialize_node(node) for node in city.nodes.values()],
            "power_grid": {
                "load": city.power_grid.load,
                "activity": city.power_grid.activity,
                "utilization": city.power_grid.utilization,
                "overloaded": city.power_grid.overloaded,
            },
        }

    def _serialize_city(self, city):
        return {
            "node_count": city.node_count,
            "building_count": city.building_count,
            "road_count": city.road_count,
            "block_count": len(city.blocks),
            "intersection_count": len(city.intersections),
            "metadata": city.metadata,
        }

    def _serialize_block(self, block):
        return {
            "id": block.id,
            "district": block.district,
            "position": list(block.position),
            "size": list(block.size),
            "building_ids": list(block.building_ids),
            "intersection_ids": list(block.intersection_ids),
            "metadata": block.metadata,
        }

    def _serialize_intersection(self, intersection):
        return {
            "id": intersection.id,
            "position": list(intersection.position),
            "road_ids": list(intersection.road_ids),
            "traffic": intersection.traffic,
            "metadata": intersection.metadata,
        }

    def _serialize_road(self, road):
        return {
            "id": road.id,
            "source_id": road.source_id,
            "destination_id": road.destination_id,
            "traffic": road.traffic,
            "active": road.active,
            "metadata": road.metadata,
        }

    def _serialize_node(self, node):
        data = {
            "id": node.id,
            "name": node.name,
            "node_type": node.node_type,
            "position": list(node.position),
            "activity": node.activity,
            "active": node.active,
            "metadata": node.metadata,
            "source_id": node.source_id,
        }

        if isinstance(node, Building):
            data.update(
                {
                    "render_type": "building",
                    "building_type": node.building_type,
                    "process_id": node.process_id,
                }
            )

        elif isinstance(node, InfrastructureNode):
            data.update(
                {
                    "render_type": "infrastructure",
                    "infrastructure_type": node.infrastructure_type,
                    "capacity": node.capacity,
                    "utilization": node.utilization,
                    "overloaded": node.overloaded,
                }
            )

        elif isinstance(node, ExternalNode):
            data.update(
                {
                    "render_type": "external",
                    "address": node.address,
                    "port": node.port,
                    "protocol": node.protocol,
                }
            )

        else:
            data["render_type"] = "generic"

        return data
