from dataclasses import dataclass, field
from typing import Any


@dataclass
class Change:
    entity_id: str
    field: str
    previous: Any
    current: Any

    @property
    def delta(self):
        if isinstance(self.previous, (int, float)) and isinstance(
            self.current, (int, float)
        ):
            return self.current - self.previous

        return None


@dataclass
class EntityCreated:
    entity_id: str
    entity: Any


@dataclass
class EntityRemoved:
    entity_id: str
    entity: Any


@dataclass
class SystemUpdate:

    process_created: list[EntityCreated] = field(default_factory=list)
    process_removed: list[EntityRemoved] = field(default_factory=list)
    process_changed: list[Change] = field(default_factory=list)

    cpu_changed: list[Change] = field(default_factory=list)

    memory_changed: list[Change] = field(default_factory=list)

    network_created: list[EntityCreated] = field(default_factory=list)
    network_removed: list[EntityRemoved] = field(default_factory=list)
    network_changed: list[Change] = field(default_factory=list)

    storage_created: list[EntityCreated] = field(default_factory=list)
    storage_removed: list[EntityRemoved] = field(default_factory=list)
    storage_changed: list[Change] = field(default_factory=list)

    gpu_created: list[EntityCreated] = field(default_factory=list)
    gpu_removed: list[EntityRemoved] = field(default_factory=list)
    gpu_changed: list[Change] = field(default_factory=list)

    sensor_created: list[EntityCreated] = field(default_factory=list)
    sensor_removed: list[EntityRemoved] = field(default_factory=list)
    sensor_changed: list[Change] = field(default_factory=list)

    @property
    def has_changes(self) -> bool:
        return any(
            [
                self.process_created,
                self.process_removed,
                self.process_changed,
                self.cpu_changed,
                self.memory_changed,
                self.network_created,
                self.network_removed,
                self.network_changed,
                self.storage_created,
                self.storage_removed,
                self.storage_changed,
                self.gpu_created,
                self.gpu_removed,
                self.gpu_changed,
                self.sensor_created,
                self.sensor_removed,
                self.sensor_changed,
            ]
        )

    @property
    def total_changes(self) -> int:
        return sum(
            [
                len(self.process_created),
                len(self.process_removed),
                len(self.process_changed),
                len(self.cpu_changed),
                len(self.memory_changed),
                len(self.network_created),
                len(self.network_removed),
                len(self.network_changed),
                len(self.storage_created),
                len(self.storage_removed),
                len(self.storage_changed),
                len(self.gpu_created),
                len(self.gpu_removed),
                len(self.gpu_changed),
                len(self.sensor_created),
                len(self.sensor_removed),
                len(self.sensor_changed),
            ]
        )
