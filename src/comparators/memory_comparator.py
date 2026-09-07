from ..snapshot.changes import Change


class MemoryComparator:

    MEMORY_THRESHOLD = 50 * 1024 * 1024  # 50 MB
    PERCENT_THRESHOLD = 5.0

    def compare(self, old, new):

        changes = []

        self._compare_numeric(
            changes, "memory", "used", old.used, new.used, self.MEMORY_THRESHOLD
        )

        self._compare_numeric(
            changes,
            "memory",
            "available",
            old.available,
            new.available,
            self.MEMORY_THRESHOLD,
        )

        self._compare_numeric(
            changes,
            "memory",
            "percent",
            old.percent,
            new.percent,
            self.PERCENT_THRESHOLD,
        )

        self._compare_numeric(
            changes,
            "memory",
            "swap_used",
            old.swap_used,
            new.swap_used,
            self.MEMORY_THRESHOLD,
        )

        self._compare_numeric(
            changes,
            "memory",
            "swap_percent",
            old.swap_percent,
            new.swap_percent,
            self.PERCENT_THRESHOLD,
        )

        return changes

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
