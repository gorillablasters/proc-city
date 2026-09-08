from ..snapshot.changes import Change, EntityCreated, EntityRemoved


class StorageComparator:

    BYTE_THRESHOLD = 10 * 1024 * 1024
    PERCENT_THRESHOLD = 5.0

    def compare(self, old, new):

        created = []
        removed = []
        changed = []

        old_devices = {storage.mountpoint: storage for storage in old}

        new_devices = {storage.mountpoint: storage for storage in new}

        for device_id in new_devices.keys() - old_devices.keys():

            created.append(
                EntityCreated(
                    entity_id=f"storage:{device_id}", entity=new_devices[device_id]
                )
            )

        for device_id in old_devices.keys() - new_devices.keys():

            removed.append(
                EntityRemoved(
                    entity_id=f"storage:{device_id}", entity=old_devices[device_id]
                )
            )

        for device_id in old_devices.keys() & new_devices.keys():

            old_storage = old_devices[device_id]
            new_storage = new_devices[device_id]

            entity_id = f"storage:{device_id}"

            self._compare_numeric(
                changed,
                entity_id,
                "used",
                old_storage.used,
                new_storage.used,
                self.BYTE_THRESHOLD,
            )

            self._compare_numeric(
                changed,
                entity_id,
                "free",
                old_storage.free,
                new_storage.free,
                self.BYTE_THRESHOLD,
            )

            self._compare_numeric(
                changed,
                entity_id,
                "percent",
                old_storage.percent,
                new_storage.percent,
                self.PERCENT_THRESHOLD,
            )

            self._compare_numeric(
                changed,
                entity_id,
                "read_bytes",
                old_storage.read_bytes,
                new_storage.read_bytes,
                self.BYTE_THRESHOLD,
            )

            self._compare_numeric(
                changed,
                entity_id,
                "write_bytes",
                old_storage.write_bytes,
                new_storage.write_bytes,
                self.BYTE_THRESHOLD,
            )

        return created, removed, changed

    @staticmethod
    def _compare_numeric(changes, entity_id, field, old_value, new_value, threshold):

        if old_value is None or new_value is None:
            return

        if abs(new_value - old_value) >= threshold:

            changes.append(
                Change(
                    entity_id=entity_id,
                    field=field,
                    previous=old_value,
                    current=new_value,
                )
            )
