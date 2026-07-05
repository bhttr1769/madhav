import ui
from task_state import (
    set_state,
    get_state,
    TaskState
)


def start(
    state,
    message
):
    set_state(state)
    ui.start_step(message)


def finish():
    ui.finish_step()
    set_state(
        TaskState.COMPLETED
    )


def fail():
    ui.finish_step()
    set_state(
        TaskState.FAILED
    )


def update(
    state,
    message
):
    finish()
    start(
        state,
        message
    )


def message(text):
    ui.smooth_lines(text)


def get_status():
    return get_state()