from ..snapshot.changes import Change, EntityCreated, EntityRemoved


class GPUComparator:

    UTILIZATION_THRESHOLD = 5.0
    MEMORY_THRESHOLD = 50 * 1024 * 1024
    TEMPERATURE_THRESHOLD = 5.0
    POWER_THRESHOLD = 10.0
    CLOCK_THRESHOLD = 100.0

    def compare(self, old, new):

        created = []
        removed = []
        changed = []

        old_gpus = {gpu.id: gpu for gpu in old}

        new_gpus = {gpu.id: gpu for gpu in new}

        for gpu_id in new_gpus.keys() - old_gpus.keys():

            created.append(
                EntityCreated(entity_id=f"gpu:{gpu_id}", entity=new_gpus[gpu_id])
            )

        for gpu_id in old_gpus.keys() - new_gpus.keys():

            removed.append(
                EntityRemoved(entity_id=f"gpu:{gpu_id}", entity=old_gpus[gpu_id])
            )

        for gpu_id in old_gpus.keys() & new_gpus.keys():

            old_gpu = old_gpus[gpu_id]
            new_gpu = new_gpus[gpu_id]

            entity_id = f"gpu:{gpu_id}"

            self._compare_numeric(
                changed,
                entity_id,
                "utilization",
                old_gpu.utilization,
                new_gpu.utilization,
                self.UTILIZATION_THRESHOLD,
            )

            self._compare_numeric(
                changed,
                entity_id,
                "memory_used",
                old_gpu.memory_used,
                new_gpu.memory_used,
                self.MEMORY_THRESHOLD,
            )

            self._compare_numeric(
                changed,
                entity_id,
                "temperature",
                old_gpu.temperature,
                new_gpu.temperature,
                self.TEMPERATURE_THRESHOLD,
            )

            self._compare_numeric(
                changed,
                entity_id,
                "power_usage",
                old_gpu.power_usage,
                new_gpu.power_usage,
                self.POWER_THRESHOLD,
            )

            self._compare_numeric(
                changed,
                entity_id,
                "clock",
                old_gpu.clock,
                new_gpu.clock,
                self.CLOCK_THRESHOLD,
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
