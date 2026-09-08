from ..city import Road, ExternalNode


class RelationshipMapper:

    def __init__(self, city):
        self.city = city

    def initialize(self, network):

        for connection in network.connections:

            self._create_connection_road(connection)

    def connection_created(self, event):

        connection = event.current

        if connection is None:
            return

        self._create_connection_road(connection)

    def connection_removed(self, event):

        road_id = self._road_id(event.entity_id)

        self.city.remove_road(road_id)

    def connection_changed(self, event):

        road_id = self._road_id(event.entity_id)

        road = self.city.get_road(road_id)

        if road is None:
            return

        road.active = event.current == "ESTABLISHED"

    def _create_connection_road(self, connection):

        road_id = self._road_id(self._connection_identifier(connection))

        source_id = self._process_id(connection.pid)

        destination_id = self._endpoint_id(connection)

        if connection.is_external:

            external = self.city.get_external(destination_id)

            if external is None:

                external = ExternalNode(
                    id=destination_id,
                    name=(f"{connection.remote_ip}:" f"{connection.remote_port}"),
                    address=connection.remote_ip,
                    port=connection.remote_port,
                    protocol=connection.protocol,
                    source_id=destination_id,
                    metadata={"status": connection.status},
                )

                self.city.add_external(external)

        existing = self.city.get_road(road_id)

        if existing:
            return existing

        road = Road(
            id=road_id,
            source_id=source_id,
            destination_id=destination_id,
            traffic=(1.0 if connection.is_established else 0.0),
            active=connection.is_established,
            metadata={
                "protocol": connection.protocol,
                "local_ip": connection.local_ip,
                "local_port": connection.local_port,
                "remote_ip": connection.remote_ip,
                "remote_port": connection.remote_port,
                "status": connection.status,
                "external": connection.is_external,
                "localhost": connection.is_localhost,
            },
        )

        self.city.add_road(road)

        return road

    @staticmethod
    def _process_id(pid):

        return f"building:process:{pid}"

    @staticmethod
    def _endpoint_id(connection):

        return f"endpoint:" f"{connection.remote_ip}:" f"{connection.remote_port}"

    @staticmethod
    def _connection_identifier(connection):

        return (
            f"{connection.pid}:"
            f"{connection.protocol}:"
            f"{connection.local_ip}:"
            f"{connection.local_port}:"
            f"{connection.remote_ip}:"
            f"{connection.remote_port}"
        )

    @staticmethod
    def _road_id(identifier):

        return f"road:{identifier}"
