from dataclasses import dataclass
from datetime import datetime

from .system import System


@dataclass
class SystemSnapshot:
    timestamp: datetime
    system: System

    @property
    def process_count(self) -> int:
        return self.system.process_count

    @property
    def cpu_load(self) -> float:
        return self.system.cpu_load

    @property
    def memory_load(self) -> float:
        return self.system.memory_load

    @property
    def network_connections(self) -> int:
        return self.system.network_connection_count
