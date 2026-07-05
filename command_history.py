_history = []


def add(command):
    _history.append(command)


def get():
    return _history.copy()


def clear():
    _history.clear()


def last():
    if _history:
        return _history[-1]

    return None