from dataclasses import dataclass


@dataclass
class Sensor:
    name: str
    sensor_type: str
    value: float
    unit: str

    @property
    def is_temperature(self) -> bool:
        return self.sensor_type.lower() == "temperature"

    @property
    def is_celsius(self) -> bool:
        return self.unit.lower() in ("c", "°c", "celsius")
