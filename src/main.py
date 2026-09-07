from .collector.system_collector import SystemCollector
from .snapshot.manager import SnapshotManager
from .snapshot.cache import SnapshotCache


def main():

    collector = SystemCollector()

    cache = SnapshotCache(max_size=10)

    manager = SnapshotManager(collector=collector, cache=cache, interval=1.0)

    try:
        manager.run()

    except KeyboardInterrupt:
        print("Stopping...")

        manager.stop()


if __name__ == "__main__":
    main()
