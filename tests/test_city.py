from src.city import City, Building, Road


def main():

    city = City()

    building_a = Building(id="building:1", name="Test Process", building_type="generic")

    building_b = Building(
        id="building:2", name="Another Process", building_type="generic"
    )

    city.add_building(building_a)
    city.add_building(building_b)

    road = Road(id="road:1", source_id=building_a.id, destination_id=building_b.id)

    city.add_road(road)

    city.power_grid.set_load(0.75)

    print(f"Buildings: {city.building_count}")

    print(f"Roads: {city.road_count}")

    print(f"Power utilization: " f"{city.power_grid.utilization}")


if __name__ == "__main__":
    main()
