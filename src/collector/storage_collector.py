import psutil

from ..decorator import aliased, alias
from ..model.storage import Storage


@aliased
class StorageCollector:
    def __init__(self):
        pass

    @alias("collect")
    def collect_storage(self) -> list[Storage]:
        disk_io = psutil.disk_io_counters()

        results = []
        for part in psutil.disk_partitions(all=False):
            if "cdrom" in part.opts or not part.fstype:
                continue

            usage = psutil.disk_usage(part.mountpoint)
            results.append(
                Storage(
                    mountpoint=part.mountpoint,
                    device=part.device,
                    fstype=part.fstype,
                    total=usage.total,
                    used=usage.used,
                    free=usage.free,
                    percent=usage.percent,
                    read_count=disk_io.read_count if disk_io else 0,
                    write_count=disk_io.write_count if disk_io else 0,
                    read_bytes=disk_io.read_bytes if disk_io else 0,
                    write_bytes=disk_io.write_bytes if disk_io else 0,
                )
            )
        return results
