from ..snapshot.changes import Change, EntityCreated, EntityRemoved


class NetworkComparator:

    BYTE_THRESHOLD = 1024 * 1024  # 1 MB
    PACKET_THRESHOLD = 100
    ERROR_THRESHOLD = 1

    def compare(self, old, new):

        created = []
        removed = []
        changed = []

        old_interfaces = {interface.name: interface for interface in old.interfaces}

        new_interfaces = {interface.name: interface for interface in new.interfaces}

        for interface_id in new_interfaces.keys() - old_interfaces.keys():

            created.append(
                EntityCreated(
                    entity_id=f"network_interface:{interface_id}",
                    entity=new_interfaces[interface_id],
                )
            )

        for interface_id in old_interfaces.keys() - new_interfaces.keys():

            removed.append(
                EntityRemoved(
                    entity_id=f"network_interface:{interface_id}",
                    entity=old_interfaces[interface_id],
                )
            )

        for interface_id in old_interfaces.keys() & new_interfaces.keys():

            old_interface = old_interfaces[interface_id]
            new_interface = new_interfaces[interface_id]

            entity_id = f"network_interface:{interface_id}"

            self._compare_numeric(
                changed,
                entity_id,
                "bytes_sent",
                old_interface.bytes_sent,
                new_interface.bytes_sent,
                self.BYTE_THRESHOLD,
            )

            self._compare_numeric(
                changed,
                entity_id,
                "bytes_received",
                old_interface.bytes_received,
                new_interface.bytes_received,
                self.BYTE_THRESHOLD,
            )

            self._compare_numeric(
                changed,
                entity_id,
                "packets_sent",
                old_interface.packets_sent,
                new_interface.packets_sent,
                self.PACKET_THRESHOLD,
            )

            self._compare_numeric(
                changed,
                entity_id,
                "packets_received",
                old_interface.packets_received,
                new_interface.packets_received,
                self.PACKET_THRESHOLD,
            )

            self._compare_numeric(
                changed,
                entity_id,
                "errors_in",
                old_interface.errors_in,
                new_interface.errors_in,
                self.ERROR_THRESHOLD,
            )

            self._compare_numeric(
                changed,
                entity_id,
                "errors_out",
                old_interface.errors_out,
                new_interface.errors_out,
                self.ERROR_THRESHOLD,
            )

            self._compare_numeric(
                changed,
                entity_id,
                "drops_in",
                old_interface.drops_in,
                new_interface.drops_in,
                self.ERROR_THRESHOLD,
            )

            self._compare_numeric(
                changed,
                entity_id,
                "drops_out",
                old_interface.drops_out,
                new_interface.drops_out,
                self.ERROR_THRESHOLD,
            )

        old_connections = {
            self._connection_id(connection): connection
            for connection in old.connections
        }

        new_connections = {
            self._connection_id(connection): connection
            for connection in new.connections
        }

        for connection_id in new_connections.keys() - old_connections.keys():

            created.append(
                EntityCreated(
                    entity_id=connection_id, entity=new_connections[connection_id]
                )
            )

        for connection_id in old_connections.keys() - new_connections.keys():

            removed.append(
                EntityRemoved(
                    entity_id=connection_id, entity=old_connections[connection_id]
                )
            )

        for connection_id in old_connections.keys() & new_connections.keys():

            old_connection = old_connections[connection_id]
            new_connection = new_connections[connection_id]

            if old_connection.status != new_connection.status:

                changed.append(
                    Change(
                        entity_id=connection_id,
                        field="status",
                        previous=old_connection.status,
                        current=new_connection.status,
                    )
                )

        return created, removed, changed

    @staticmethod
    def _connection_id(connection):

        return (
            f"connection:"
            f"{connection.pid}:"
            f"{connection.protocol}:"
            f"{connection.local_ip}:"
            f"{connection.local_port}:"
            f"{connection.remote_ip}:"
            f"{connection.remote_port}"
        )

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
