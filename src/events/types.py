from enum import Enum


class EventCategory(Enum):

    LIFECYCLE = "lifecycle"
    ACTIVITY = "activity"
    STATE = "state"
    RELATIONSHIP = "relationship"


class EventType(Enum):

    PROCESS_CREATED = "process_created"
    PROCESS_TERMINATED = "process_terminated"
    PROCESS_STARTED = "process_started"
    PROCESS_STOPPED = "process_stopped"

    PROCESS_CPU_ACTIVITY = "process_cpu_activity"
    PROCESS_MEMORY_ACTIVITY = "process_memory_activity"
    PROCESS_IO_ACTIVITY = "process_io_activity"

    CPU_SPIKE = "cpu_spike"
    CPU_LOAD_CHANGED = "cpu_load_changed"

    MEMORY_PRESSURE_INCREASED = "memory_pressure_increased"
    MEMORY_PRESSURE_DECREASED = "memory_pressure_decreased"

    NETWORK_CONNECTION_CREATED = "network_connection_created"
    NETWORK_CONNECTION_REMOVED = "network_connection_removed"
    NETWORK_CONNECTION_STATUS_CHANGED = "network_connection_status_changed"

    NETWORK_ACTIVITY = "network_activity"

    STORAGE_CREATED = "storage_created"
    STORAGE_REMOVED = "storage_removed"

    STORAGE_ACTIVITY = "storage_activity"
    STORAGE_NEAR_CAPACITY = "storage_near_capacity"

    GPU_CREATED = "gpu_created"
    GPU_REMOVED = "gpu_removed"

    GPU_HIGH_UTILIZATION = "gpu_high_utilization"
    GPU_ACTIVITY = "gpu_activity"

    SENSOR_CREATED = "sensor_created"
    SENSOR_REMOVED = "sensor_removed"

    SENSOR_VALUE_CHANGED = "sensor_value_changed"


EVENT_CATEGORIES = {
    EventType.PROCESS_CREATED: EventCategory.LIFECYCLE,
    EventType.PROCESS_TERMINATED: EventCategory.LIFECYCLE,
    EventType.PROCESS_STARTED: EventCategory.STATE,
    EventType.PROCESS_STOPPED: EventCategory.STATE,
    EventType.PROCESS_CPU_ACTIVITY: EventCategory.ACTIVITY,
    EventType.PROCESS_MEMORY_ACTIVITY: EventCategory.ACTIVITY,
    EventType.PROCESS_IO_ACTIVITY: EventCategory.ACTIVITY,
    EventType.CPU_SPIKE: EventCategory.ACTIVITY,
    EventType.CPU_LOAD_CHANGED: EventCategory.STATE,
    EventType.MEMORY_PRESSURE_INCREASED: EventCategory.STATE,
    EventType.MEMORY_PRESSURE_DECREASED: EventCategory.STATE,
    EventType.NETWORK_CONNECTION_CREATED: EventCategory.RELATIONSHIP,
    EventType.NETWORK_CONNECTION_REMOVED: EventCategory.RELATIONSHIP,
    EventType.NETWORK_CONNECTION_STATUS_CHANGED: EventCategory.STATE,
    EventType.NETWORK_ACTIVITY: EventCategory.ACTIVITY,
    EventType.STORAGE_CREATED: EventCategory.LIFECYCLE,
    EventType.STORAGE_REMOVED: EventCategory.LIFECYCLE,
    EventType.STORAGE_ACTIVITY: EventCategory.ACTIVITY,
    EventType.STORAGE_NEAR_CAPACITY: EventCategory.STATE,
    EventType.GPU_CREATED: EventCategory.LIFECYCLE,
    EventType.GPU_REMOVED: EventCategory.LIFECYCLE,
    EventType.GPU_HIGH_UTILIZATION: EventCategory.ACTIVITY,
    EventType.GPU_ACTIVITY: EventCategory.ACTIVITY,
    EventType.SENSOR_CREATED: EventCategory.LIFECYCLE,
    EventType.SENSOR_REMOVED: EventCategory.LIFECYCLE,
    EventType.SENSOR_VALUE_CHANGED: EventCategory.STATE,
}
