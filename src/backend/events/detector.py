from datetime import datetime

from .event import SystemEvent


class EventDetector:

    CPU_SPIKE_THRESHOLD = 30.0
    MEMORY_PRESSURE_THRESHOLD = 10.0

    def detect(self, update):

        events = []

        events.extend(self._detect_process_events(update))

        events.extend(self._detect_cpu_events(update))

        events.extend(self._detect_memory_events(update))

        events.extend(self._detect_network_events(update))

        events.extend(self._detect_storage_events(update))

        events.extend(self._detect_gpu_events(update))

        events.extend(self._detect_sensor_events(update))

        return events

    def _detect_process_events(self, update):

        events = []

        for created in update.process_created:

            events.append(
                SystemEvent(
                    timestamp=datetime.now(),
                    event_type="PROCESS_CREATED",
                    source="process",
                    entity_id=created.entity_id,
                    current=created.entity,
                )
            )

        for removed in update.process_removed:

            events.append(
                SystemEvent(
                    timestamp=datetime.now(),
                    event_type="PROCESS_TERMINATED",
                    source="process",
                    entity_id=removed.entity_id,
                    previous=removed.entity,
                )
            )

        for change in update.process_changed:

            event_type = None

            if change.field == "status":

                if change.current == "running":
                    event_type = "PROCESS_STARTED"

                elif change.previous == "running":
                    event_type = "PROCESS_STOPPED"

            if event_type:

                events.append(
                    SystemEvent(
                        timestamp=datetime.now(),
                        event_type=event_type,
                        source="process",
                        entity_id=change.entity_id,
                        previous=change.previous,
                        current=change.current,
                        delta=change.delta,
                    )
                )

        return events

    def _detect_cpu_events(self, update):

        events = []

        for change in update.cpu_changed:

            if change.field == "overall_percent":

                if (
                    change.delta is not None
                    and change.delta >= self.CPU_SPIKE_THRESHOLD
                ):

                    events.append(
                        SystemEvent(
                            timestamp=datetime.now(),
                            event_type="CPU_SPIKE",
                            source="cpu",
                            entity_id=change.entity_id,
                            previous=change.previous,
                            current=change.current,
                            delta=change.delta,
                        )
                    )

        return events

    def _detect_memory_events(self, update):

        events = []

        for change in update.memory_changed:

            if change.field == "percent":

                if (
                    change.delta is not None
                    and change.delta >= self.MEMORY_PRESSURE_THRESHOLD
                ):

                    events.append(
                        SystemEvent(
                            timestamp=datetime.now(),
                            event_type="MEMORY_PRESSURE_INCREASED",
                            source="memory",
                            entity_id=change.entity_id,
                            previous=change.previous,
                            current=change.current,
                            delta=change.delta,
                        )
                    )

        return events

    def _detect_network_events(self, update):

        events = []

        for created in update.network_created:

            if created.entity_id.startswith("connection:"):

                events.append(
                    SystemEvent(
                        timestamp=datetime.now(),
                        event_type="NETWORK_CONNECTION_CREATED",
                        source="network",
                        entity_id=created.entity_id,
                        current=created.entity,
                    )
                )

        for removed in update.network_removed:

            if removed.entity_id.startswith("connection:"):

                events.append(
                    SystemEvent(
                        timestamp=datetime.now(),
                        event_type="NETWORK_CONNECTION_REMOVED",
                        source="network",
                        entity_id=removed.entity_id,
                        previous=removed.entity,
                    )
                )

        for change in update.network_changed:

            if change.field == "status":

                events.append(
                    SystemEvent(
                        timestamp=datetime.now(),
                        event_type="NETWORK_CONNECTION_STATUS_CHANGED",
                        source="network",
                        entity_id=change.entity_id,
                        previous=change.previous,
                        current=change.current,
                        delta=change.delta,
                    )
                )

        return events

    def _detect_storage_events(self, update):

        events = []

        for change in update.storage_changed:

            if change.field == "percent":

                if change.current is not None and change.current >= 90:

                    events.append(
                        SystemEvent(
                            timestamp=datetime.now(),
                            event_type="STORAGE_NEAR_CAPACITY",
                            source="storage",
                            entity_id=change.entity_id,
                            previous=change.previous,
                            current=change.current,
                            delta=change.delta,
                        )
                    )

        return events

    def _detect_gpu_events(self, update):

        events = []

        for change in update.gpu_changed:

            if change.field == "utilization":

                if change.current is not None and change.current >= 90:

                    events.append(
                        SystemEvent(
                            timestamp=datetime.now(),
                            event_type="GPU_HIGH_UTILIZATION",
                            source="gpu",
                            entity_id=change.entity_id,
                            previous=change.previous,
                            current=change.current,
                            delta=change.delta,
                        )
                    )

        return events

    def _detect_sensor_events(self, update):

        events = []

        for change in update.sensor_changed:

            if change.field == "value":

                events.append(
                    SystemEvent(
                        timestamp=datetime.now(),
                        event_type="SENSOR_VALUE_CHANGED",
                        source="sensor",
                        entity_id=change.entity_id,
                        previous=change.previous,
                        current=change.current,
                        delta=change.delta,
                    )
                )

        return events
