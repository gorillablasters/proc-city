import json
from pathlib import Path

from backend.snapshot.manager import SnapshotManager
from backend.mapping.mapper import CityMapper
from backend.server.serializer import CitySerializer


def main():

    snapshot_manager = SnapshotManager()

    snapshot = snapshot_manager.collect()

    mapper = CityMapper()

    city = mapper.initialize(snapshot)

    serializer = CitySerializer()

    data = serializer.serialize(city)

    city_json_file = Path(__file__).parent.parent / "src/web/public" / "city.json"
    with open(city_json_file, "w", encoding="utf-8") as file:

        json.dump(data, file, indent=2)

    print("City exported successfully.")

    print(f"Processes: {len(snapshot.system.processes)}")

    print(f"City nodes: {city.node_count}")

    print(f"Buildings: {city.building_count}")

    print(f"Blocks: {len(city.blocks)}")

    print(f"Intersections: {len(city.intersections)}")

    print(f"Roads: {len(city.roads)}")


if __name__ == "__main__":
    main()
