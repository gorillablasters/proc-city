from ..snapshot.changes import Change


class CPUComparator:

    PERCENT_THRESHOLD = 5.0
    FREQUENCY_THRESHOLD = 100.0
    LOAD_THRESHOLD = 0.25

    def compare(self, old, new):

        changes = []

        self._compare_numeric(
            changes,
            "cpu",
            "overall_percent",
            old.overall_percent,
            new.overall_percent,
            self.PERCENT_THRESHOLD,
        )

        self._compare_numeric(
            changes,
            "cpu",
            "frequency_current",
            old.frequency_current,
            new.frequency_current,
            self.FREQUENCY_THRESHOLD,
        )

        self._compare_numeric(
            changes, "cpu", "load_1m", old.load_1m, new.load_1m, self.LOAD_THRESHOLD
        )

        self._compare_numeric(
            changes, "cpu", "load_5m", old.load_5m, new.load_5m, self.LOAD_THRESHOLD
        )

        self._compare_numeric(
            changes, "cpu", "load_15m", old.load_15m, new.load_15m, self.LOAD_THRESHOLD
        )

        if old.per_core_percent != new.per_core_percent:

            if len(old.per_core_percent) == len(new.per_core_percent):

                for index, (old_value, new_value) in enumerate(
                    zip(old.per_core_percent, new.per_core_percent)
                ):

                    self._compare_numeric(
                        changes,
                        "cpu",
                        f"core_{index}_percent",
                        old_value,
                        new_value,
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
