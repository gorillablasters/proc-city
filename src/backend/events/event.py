from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Optional

from .types import EventType, EventCategory, EVENT_CATEGORIES


@dataclass
class SystemEvent:

    timestamp: datetime

    event_type: EventType

    source: str

    entity_id: Optional[str] = None

    previous: Any = None
    current: Any = None
    delta: Any = None

    metadata: dict = field(default_factory=dict)

    @property
    def category(self) -> EventCategory:
        return EVENT_CATEGORIES[self.event_type]

    @property
    def has_delta(self) -> bool:
        return self.delta is not None

    @property
    def magnitude(self) -> float:

        if self.delta is None:
            return 1.0

        try:
            return abs(float(self.delta))
        except (TypeError, ValueError):
            return 1.0
