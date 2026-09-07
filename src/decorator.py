class alias:
    def __init__(self, *names):
        self.names = names

    def __call__(self, f):
        f._aliases = self.names
        return f


def aliased(cls):
    for name, method in cls.__dict__.copy().items():
        if hasattr(method, "_aliases"):
            for a in method._aliases:
                setattr(cls, a, method)
    return cls
