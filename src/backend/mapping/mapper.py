from ..city import City, Building
from ..events.types import EventType

from .classifier import ProcessClassifier
from .rules import get_building_type
from .relationships import RelationshipMapper
from .layout import CityLayout
from ..city.infrastructure import InfrastructureNode
from .topology import CityTopologyBuilder


class CityMapper:

    def __init__(self, city=None):
        self.city = city or City()

        self.classifier = ProcessClassifier()

        self.relationships = RelationshipMapper(self.city)

        self.layout = CityLayout()

        self.topology = CityTopologyBuilder()

    def initialize(self, snapshot):

        system = snapshot.system

        self.topology.build(self.city)

        for process in system.processes:

            self._create_process_building(process)

        self.relationships.initialize(system.network)

        self._create_infrastructure(system)

        self._update_resources(system)

        self.layout.layout(self.city)

    def apply_events(self, events):

        for event in events:
            self.apply_event(event)

    def apply_event(self, event):

        event_type = event.event_type

        if event_type == EventType.PROCESS_CREATED:
            self._handle_process_created(event)

        elif event_type == EventType.PROCESS_TERMINATED:
            self._handle_process_terminated(event)

        elif event_type == EventType.PROCESS_CPU_ACTIVITY:
            self._handle_process_activity(event)

        elif event_type == EventType.PROCESS_MEMORY_ACTIVITY:
            self._handle_process_activity(event)

        elif event_type == EventType.PROCESS_IO_ACTIVITY:
            self._handle_process_activity(event)

        elif event_type == EventType.CPU_SPIKE:
            self._handle_cpu_spike(event)

        elif event_type == EventType.CPU_LOAD_CHANGED:
            self._handle_cpu_load(event)

        elif event_type == EventType.NETWORK_CONNECTION_CREATED:
            self.relationships.connection_created(event)

        elif event_type == EventType.NETWORK_CONNECTION_REMOVED:
            self.relationships.connection_removed(event)

        elif event_type == EventType.NETWORK_CONNECTION_STATUS_CHANGED:
            self.relationships.connection_changed(event)

    def _create_infrastructure(self, system):

        cpu = InfrastructureNode(
            id="infrastructure:cpu",
            name="CPU",
            infrastructure_type="cpu",
            utilization=(system.cpu.overall_percent / 100.0),
            source_id="cpu",
            metadata={
                "physical_cores": system.cpu.physical_cores,
                "logical_cores": system.cpu.logical_cores,
                "frequency": system.cpu.frequency_current,
            },
        )

        cpu.set_utilization(system.cpu.overall_percent / 100.0)

        self.city.add_infrastructure(cpu)

        memory = InfrastructureNode(
            id="infrastructure:memory",
            name="Memory",
            infrastructure_type="memory",
            source_id="memory",
            metadata={
                "total": system.memory.total,
                "used": system.memory.used,
                "available": system.memory.available,
                "percent": system.memory.percent,
            },
        )

        memory.set_utilization(system.memory.percent / 100.0)

        self.city.add_infrastructure(memory)

        for gpu in system.gpus:

            gpu_node = InfrastructureNode(
                id=f"infrastructure:gpu:{gpu.id}",
                name=gpu.name,
                infrastructure_type="gpu",
                source_id=str(gpu.id),
                metadata={
                    "memory_total": gpu.memory_total,
                    "memory_used": gpu.memory_used,
                    "temperature": gpu.temperature,
                    "power_usage": gpu.power_usage,
                    "clock": gpu.clock,
                },
            )

            gpu_node.set_utilization(gpu.utilization / 100.0)

            self.city.add_infrastructure(gpu_node)

        for storage in system.storage:

            storage_id = (
                f"infrastructure:"
                f"storage:"
                f"{storage.device}:"
                f"{storage.mountpoint}"
            )

            storage_node = InfrastructureNode(
                id=storage_id,
                name=storage.device,
                infrastructure_type="storage",
                source_id=storage.device,
                metadata={
                    "mountpoint": storage.mountpoint,
                    "total": storage.total,
                    "used": storage.used,
                    "free": storage.free,
                    "percent": storage.percent,
                },
            )

            storage_node.set_utilization(storage.percent / 100.0)

            self.city.add_infrastructure(storage_node)

    def _create_process_building(self, process):

        building_id = self._process_building_id(process.stable_id)

        if self.city.get_building(building_id):
            return self.city.get_building(building_id)

        classification = self.classifier.classify(process)

        building_type = get_building_type(classification.category)

        building = Building(
            id=building_id,
            name=process.name,
            building_type=building_type,
            process_id=process.stable_id,
            active=True,
            metadata={
                "pid": process.pid,
                "category": classification.category,
                "confidence": classification.confidence,
                "executable": process.executable,
                "username": process.username,
            },
        )

        building.set_activity(self._process_activity(process))

        self.city.add_building(building)

        return building

    def _handle_process_created(self, event):

        process = event.current

        if process is None:
            return

        self._create_process_building(process)

        self.layout.layout(self.city)

    def _handle_process_terminated(self, event):

        process_id = event.entity_id

        building_id = self._process_building_id(process_id)

        building = self.city.get_building(building_id)

        if building is None:
            return

        building.active = False
        building.set_activity(0.0)

    def _handle_process_activity(self, event):

        process_id = event.entity_id

        building_id = self._process_building_id(process_id)

        building = self.city.get_building(building_id)

        if building is None:
            return

        building.active = True

        building.set_activity(self._event_activity(event))

    def _handle_cpu_spike(self, event):

        magnitude = event.magnitude

        activity = min(1.0, magnitude / 100.0)

        self.city.power_grid.set_load(activity)

    def _handle_cpu_load(self, event):

        current = event.current

        if current is None:
            return

        try:
            load = float(current) / 100.0
        except (TypeError, ValueError):
            return

        self.city.power_grid.set_load(load)

    def _update_resources(self, system):

        if system.cpu:
            self.city.power_grid.set_load(system.cpu.overall_percent / 100.0)
            cpu_node = self.city.get_infrastructure("infrastructure:cpu")

            if cpu_node:
                cpu_node.set_utilization(system.cpu.overall_percent / 100.0)

        memory_node = self.city.get_infrastructure("infrastructure:memory")

        if memory_node:
            memory_node.set_utilization(system.memory.percent / 100.0)

        for gpu in system.gpus:

            gpu_node = self.city.get_infrastructure(f"infrastructure:gpu:{gpu.id}")

            if gpu_node:
                gpu_node.set_utilization(gpu.utilization / 100.0)

        for storage in system.storage:

            storage_id = (
                f"infrastructure:storage:" f"{storage.device}:" f"{storage.mountpoint}"
            )

            storage_node = self.city.get_infrastructure(storage_id)

            if storage_node:
                storage_node.set_utilization(storage.percent / 100.0)

    @staticmethod
    def _process_building_id(process_id):

        return f"building:{process_id}"

    @staticmethod
    def _process_activity(process):

        cpu = min(process.cpu_percent / 100.0, 1.0)

        memory = min(process.memory_percent / 100.0, 1.0)

        network = min(process.connections / 10.0, 1.0)

        io = min(process.total_io_bytes / (100 * 1024 * 1024), 1.0)

        return max(cpu, memory, network, io)

    @staticmethod
    def _event_activity(event):

        magnitude = event.magnitude

        return min(1.0, magnitude / 100.0)
