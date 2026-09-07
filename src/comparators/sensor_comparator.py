from ..snapshot.changes import Change, EntityCreated, EntityRemoved


class SensorComparator:

    VALUE_THRESHOLD = 1.0

    def compare(self, old, new):

        created = []
        removed = []
        changed = []

        old_sensors = {sensor.name: sensor for sensor in old}

        new_sensors = {sensor.name: sensor for sensor in new}

        for sensor_id in new_sensors.keys() - old_sensors.keys():

            created.append(
                EntityCreated(
                    entity_id=f"sensor:{sensor_id}", entity=new_sensors[sensor_id]
                )
            )

        for sensor_id in old_sensors.keys() - new_sensors.keys():

            removed.append(
                EntityRemoved(
                    entity_id=f"sensor:{sensor_id}", entity=old_sensors[sensor_id]
                )
            )

        for sensor_id in old_sensors.keys() & new_sensors.keys():

            old_sensor = old_sensors[sensor_id]
            new_sensor = new_sensors[sensor_id]

            entity_id = f"sensor:{sensor_id}"

            if old_sensor.value is not None and new_sensor.value is not None:

                if abs(new_sensor.value - old_sensor.value) >= self.VALUE_THRESHOLD:

                    changed.append(
                        Change(
                            entity_id=entity_id,
                            field="value",
                            previous=old_sensor.value,
                            current=new_sensor.value,
                        )
                    )

            if old_sensor.unit != new_sensor.unit:

                changed.append(
                    Change(
                        entity_id=entity_id,
                        field="unit",
                        previous=old_sensor.unit,
                        current=new_sensor.unit,
                    )
                )

        return created, removed, changed
