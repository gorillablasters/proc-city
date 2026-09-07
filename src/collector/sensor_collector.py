import psutil

from ..decorator import aliased, alias
from ..model.sensor import Sensor


@aliased
class SensorCollector:
    def __init__(self):
        pass

    @alias("collect")
    def collect_sensors(self) -> list[Sensor]:
        sensors: list[Sensor] = []

        try:
            temps = psutil.sensors_temperatures()
            for chip, entries in temps.items():
                for entry in entries:
                    label = entry.label or chip
                    sensors.append(
                        Sensor(
                            name=f"{chip} {label}".strip(),
                            sensor_type="temperature",
                            value=entry.current,
                            unit="°C",
                        )
                    )
        except (AttributeError, NotImplementedError):
            pass

        try:
            fans = psutil.sensors_fans()
            for chip, entries in fans.items():
                for entry in entries:
                    label = entry.label or chip
                    sensors.append(
                        Sensor(
                            name=f"{chip} {label}".strip(),
                            sensor_type="fan",
                            value=float(entry.current),
                            unit="RPM",
                        )
                    )
        except (AttributeError, NotImplementedError):
            pass

        try:
            bat = psutil.sensors_battery()
            if bat:
                sensors.append(
                    Sensor(
                        name="battery",
                        sensor_type="battery",
                        value=bat.percent,
                        unit="%",
                    )
                )
        except (AttributeError, NotImplementedError):
            pass

        return sensors
