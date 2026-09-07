from ..snapshot.changes import Change, EntityCreated, EntityRemoved


class ProcessComparator:

    CPU_THRESHOLD = 5.0
    MEMORY_THRESHOLD = 10 * 1024 * 1024  # 10 MB
    THREAD_THRESHOLD = 1
    IO_THRESHOLD = 1024 * 1024  # 1 MB

    def compare(self, previous, current):

        previous_map = {p.stable_id: p for p in previous}

        current_map = {p.stable_id: p for p in current}

        created = []
        removed = []
        changed = []

        for process_id in current_map.keys() - previous_map.keys():

            created.append(
                EntityCreated(entity_id=process_id, entity=current_map[process_id])
            )

        for process_id in previous_map.keys() - current_map.keys():

            removed.append(
                EntityRemoved(entity_id=process_id, entity=previous_map[process_id])
            )

        for process_id in current_map.keys() & previous_map.keys():

            old = previous_map[process_id]
            new = current_map[process_id]

            changed.extend(self.compare_process(old, new))

        return created, removed, changed

    def compare_process(self, old, new):

        changes = []

        self._compare_numeric(
            changes,
            new,
            "cpu_percent",
            old.cpu_percent,
            new.cpu_percent,
            self.CPU_THRESHOLD,
        )

        self._compare_numeric(
            changes,
            new,
            "memory_rss",
            old.memory_rss,
            new.memory_rss,
            self.MEMORY_THRESHOLD,
        )

        self._compare_numeric(
            changes, new, "threads", old.threads, new.threads, self.THREAD_THRESHOLD
        )

        self._compare_numeric(
            changes,
            new,
            "read_bytes",
            old.read_bytes,
            new.read_bytes,
            self.IO_THRESHOLD,
        )

        self._compare_numeric(
            changes,
            new,
            "write_bytes",
            old.write_bytes,
            new.write_bytes,
            self.IO_THRESHOLD,
        )

        if old.status != new.status:

            changes.append(
                Change(
                    entity_id=new.stable_id,
                    field="status",
                    previous=old.status,
                    current=new.status,
                )
            )

        return changes

    @staticmethod
    def _compare_numeric(changes, process, field, old_value, new_value, threshold):

        if old_value is None or new_value is None:
            return

        if abs(new_value - old_value) >= threshold:

            changes.append(
                Change(
                    entity_id=process.stable_id,
                    field=field,
                    previous=old_value,
                    current=new_value,
                )
            )
