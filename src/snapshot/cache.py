class SnapshotCache:

    def __init__(self, max_size=10):
        self.max_size = max_size
        self.snapshots = []

    def add(self, snapshot):
        self.snapshots.append(snapshot)

        if len(self.snapshots) > self.max_size:
            self.snapshots.pop(0)

    @property
    def latest(self):
        if not self.snapshots:
            return None

        return self.snapshots[-1]
