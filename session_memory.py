_memory = {}


def set(
    key,
    value
):
    _memory[key] = value


def get(
    key,
    default=None
):
    return _memory.get(
        key,
        default
    )


def has(
    key
):
    return key in _memory


def remove(
    key
):
    if key in _memory:
        del _memory[key]


def clear():
    _memory.clear()


def all():
    return _memory.copy()