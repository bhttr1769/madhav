class TaskState:
    IDLE = "IDLE"
    PLANNING = "PLANNING"
    GENERATING = "GENERATING"
    READING = "READING"
    EXECUTING = "EXECUTING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


current_state = TaskState.IDLE


def set_state(state):
    global current_state
    current_state = state


def get_state():
    return current_state