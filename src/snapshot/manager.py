import time
from datetime import datetime

from ..comparators.comparator import SnapshotComparator
from ..events.detector import EventDetector
from ..model.snapshot import SystemSnapshot


class SnapshotManager:

    def __init__(self, collector, cache, interval=1.0):
        self.collector = collector
        self.cache = cache
        self.interval = interval

        self.comparator = SnapshotComparator()
        self.event_detector = EventDetector()

        self.running = False

    def collect(self):

        system = self.collector.collect()

        return SystemSnapshot(timestamp=datetime.now(), system=system)

    def run(self):

        self.running = True

        while self.running:

            start = time.monotonic()

            current = self.collect()

            previous = self.cache.latest

            if previous is None:

                print("Initial snapshot")

            else:

                update = self.comparator.compare(previous, current)

                if update.has_changes:
                    self.handle_update(update)
                    events = self.event_detector.detect(update)
                    self.handle_events(events)

            self.cache.add(current)

            elapsed = time.monotonic() - start

            sleep_time = max(0, self.interval - elapsed)

            time.sleep(sleep_time)

    def handle_events(self, events):

        for event in events:

            print(
                f"[EVENT] "
                f"{event.event_type} "
                f"source={event.source} "
                f"entity={event.entity_id}"
            )

    def handle_update(self, update):

        print("\n===== SYSTEM UPDATE =====")

        if update.process_created:
            print(f"Processes created: " f"{len(update.process_created)}")

        if update.process_removed:
            print(f"Processes removed: " f"{len(update.process_removed)}")

        if update.process_changed:
            print(f"Process changes: " f"{len(update.process_changed)}")

        if update.cpu_changed:
            print(f"CPU changes: " f"{len(update.cpu_changed)}")

            for change in update.cpu_changed:
                print(
                    f"  CPU {change.field}: " f"{change.previous} -> {change.current}"
                )

        if update.memory_changed:
            print(f"Memory changes: " f"{len(update.memory_changed)}")

            for change in update.memory_changed:
                print(
                    f"  Memory {change.field}: "
                    f"{change.previous} -> {change.current}"
                )

        if update.network_created:
            print(f"Network entities created: " f"{len(update.network_created)}")

        if update.network_removed:
            print(f"Network entities removed: " f"{len(update.network_removed)}")

        if update.network_changed:
            print(f"Network changes: " f"{len(update.network_changed)}")

        if update.storage_changed:
            print(f"Storage changes: " f"{len(update.storage_changed)}")

        if update.gpu_changed:
            print(f"GPU changes: " f"{len(update.gpu_changed)}")

        if update.sensor_changed:
            print(f"Sensor changes: " f"{len(update.sensor_changed)}")

        print(f"Total changes: {update.total_changes}")

        print("=========================\n")

    def stop(self):
        self.running = False
