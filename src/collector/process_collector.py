import psutil

from ..decorator import aliased, alias
from ..model.process import Process


@aliased
class ProcessCollector:
    def __init__(self):
        self.iter_list = [
            "pid",
            "ppid",
            "name",
            "exe",
            "username",
            "status",
            "create_time",
            "cpu_percent",
            "cpu_times",
            "num_threads",
            "memory_info",
            "memory_percent",
            "io_counters",
            "nice",
            "net_connections",
        ]

    @alias("collect")
    def collect_processes(self) -> list[Process]:
        processes = []
        for proc in psutil.process_iter(self.iter_list):
            try:
                pinfo = proc.info
                process = Process(
                    pid=pinfo["pid"],
                    parent_pid=pinfo["ppid"],
                    name=pinfo["name"],
                    executable=pinfo.get("exe"),
                    username=pinfo.get("username"),
                    status=pinfo["status"],
                    create_time=pinfo["create_time"],
                    cpu_percent=pinfo["cpu_percent"],
                    cpu_user_time=(
                        pinfo["cpu_times"].user if pinfo.get("cpu_times") else 0.0
                    ),
                    cpu_system_time=(
                        pinfo["cpu_times"].system if pinfo.get("cpu_times") else 0.0
                    ),
                    threads=pinfo["num_threads"],
                    memory_rss=(
                        pinfo["memory_info"].rss if pinfo.get("memory_info") else 0
                    ),
                    memory_vms=(
                        pinfo["memory_info"].vms if pinfo.get("memory_info") else 0
                    ),
                    memory_percent=(
                        pinfo["memory_percent"] if pinfo.get("memory_percent") else 0.0
                    ),
                    read_count=(
                        pinfo["io_counters"].read_count
                        if pinfo.get("io_counters")
                        else 0
                    ),
                    write_count=(
                        pinfo["io_counters"].write_count
                        if pinfo.get("io_counters")
                        else 0
                    ),
                    read_bytes=(
                        pinfo["io_counters"].read_bytes
                        if pinfo.get("io_counters")
                        else 0
                    ),
                    write_bytes=(
                        pinfo["io_counters"].write_bytes
                        if pinfo.get("io_counters")
                        else 0
                    ),
                    nice=pinfo.get("nice"),
                    connections=(
                        len(pinfo["net_connections"])
                        if pinfo.get("net_connections")
                        else 0
                    ),
                )
                processes.append(process)
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue
        return processes
