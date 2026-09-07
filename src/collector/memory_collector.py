import psutil

from ..model.memory import Memory


def collect_memory() -> Memory:

    virtual_memory = psutil.virtual_memory()
    swap_memory = psutil.swap_memory()

    memory = Memory(
        total=virtual_memory.total,
        available=virtual_memory.available,
        used=virtual_memory.used,
        percent=virtual_memory.percent,
        swap_total=swap_memory.total,
        swap_used=swap_memory.used,
        swap_free=swap_memory.free,
        swap_percent=swap_memory.percent,
    )

    return memory
