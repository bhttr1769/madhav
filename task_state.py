class TaskState:
    IDLE = "IDLE"
    PLANNING = "PLANNING"
    GENERATING = "GENERATING"
    READING = "READING"
    EXECUTING = "EXECUTING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


_current_state = TaskState.IDLE


def set_state(state):
    global _current_state
    _current_state = state


def get_state():
    return _current_state