import psutil

from ..model.network import Network, NetworkInterface, NetworkConnection


def collect_network() -> Network:
    network_interfaces = []
    for interface_name, _ in psutil.net_if_stats().items():
        network_interfaces.append(
            NetworkInterface(
                name=interface_name,
                bytes_sent=psutil.net_io_counters(pernic=True)[
                    interface_name
                ].bytes_sent,
                bytes_received=psutil.net_io_counters(pernic=True)[
                    interface_name
                ].bytes_recv,
                packets_sent=psutil.net_io_counters(pernic=True)[
                    interface_name
                ].packets_sent,
                packets_received=psutil.net_io_counters(pernic=True)[
                    interface_name
                ].packets_recv,
                errors_in=psutil.net_io_counters(pernic=True)[interface_name].errin,
                errors_out=psutil.net_io_counters(pernic=True)[interface_name].errout,
                drops_in=psutil.net_io_counters(pernic=True)[interface_name].dropin,
                drops_out=psutil.net_io_counters(pernic=True)[interface_name].dropout,
            )
        )
        network_connections = []
    for conn in psutil.net_connections():
        network_connections.append(
            NetworkConnection(
                pid=conn.pid,
                protocol=conn.type.name,
                local_ip=conn.laddr.ip if conn.laddr else None,
                local_port=conn.laddr.port if conn.laddr else None,
                remote_ip=conn.raddr.ip if conn.raddr else None,
                remote_port=conn.raddr.port if conn.raddr else None,
                status=conn.status,
            )
        )
    network = Network(
        interfaces=network_interfaces,
        connections=network_connections,
    )

    return network
