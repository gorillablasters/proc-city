from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class NetworkInterface:
    name: str

    bytes_sent: int
    bytes_received: int

    packets_sent: int
    packets_received: int

    errors_in: int
    errors_out: int

    drops_in: int
    drops_out: int

    @property
    def total_bytes(self) -> int:
        return self.bytes_sent + self.bytes_received

    @property
    def total_packets(self) -> int:
        return self.packets_sent + self.packets_received

    @property
    def total_errors(self) -> int:
        return self.errors_in + self.errors_out

    @property
    def total_drops(self) -> int:
        return self.drops_in + self.drops_out

    @property
    def has_errors(self) -> bool:
        return self.total_errors > 0

    @property
    def has_drops(self) -> bool:
        return self.total_drops > 0


@dataclass
class NetworkConnection:
    pid: Optional[int]
    creation_time: datetime

    protocol: str

    local_ip: str
    local_port: int

    remote_ip: Optional[str]
    remote_port: Optional[int]

    status: str

    @property
    def is_localhost(self) -> bool:
        return self.remote_ip in (
            "127.0.0.1",
            "::1",
            "localhost",
        )

    @property
    def is_external(self) -> bool:
        return self.remote_ip is not None and not self.is_localhost

    @property
    def is_established(self) -> bool:
        return self.status.upper() == "ESTABLISHED"

    @property
    def is_listening(self) -> bool:
        return self.status.upper() == "LISTEN"

    @property
    def endpoint(self) -> str:
        remote = f"{self.remote_ip}:{self.remote_port}" if self.remote_ip else "unknown"

        return f"{self.local_ip}:{self.local_port} -> {remote}"


@dataclass
class Network:
    interfaces: list[NetworkInterface]
    connections: list[NetworkConnection]

    @property
    def interface_count(self) -> int:
        return len(self.interfaces)

    @property
    def connection_count(self) -> int:
        return len(self.connections)

    @property
    def active_connections(self) -> list[NetworkConnection]:
        return [
            connection for connection in self.connections if connection.is_established
        ]

    @property
    def external_connections(self) -> list[NetworkConnection]:
        return [connection for connection in self.connections if connection.is_external]

    @property
    def localhost_connections(self) -> list[NetworkConnection]:
        return [
            connection for connection in self.connections if connection.is_localhost
        ]

    @property
    def total_bytes(self) -> int:
        return sum(interface.total_bytes for interface in self.interfaces)

    @property
    def total_packets(self) -> int:
        return sum(interface.total_packets for interface in self.interfaces)
