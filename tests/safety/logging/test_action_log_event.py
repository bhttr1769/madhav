from brain.safety.logging.models.action_log_event import (
    ActionLogEvent,
)


def test_action_log_event_values():

    assert (
        ActionLogEvent.REQUESTED.value
        == "requested"
    )

    assert (
        ActionLogEvent.EVALUATED.value
        == "evaluated"
    )

    assert (
        ActionLogEvent.APPROVAL_GRANTED.value
        == "approval_granted"
    )

    assert (
        ActionLogEvent.APPROVAL_REJECTED.value
        == "approval_rejected"
    )

    assert (
        ActionLogEvent.EXECUTION_STARTED.value
        == "execution_started"
    )

    assert (
        ActionLogEvent.EXECUTION_COMPLETED.value
        == "execution_completed"
    )

    assert (
        ActionLogEvent.EXECUTION_FAILED.value
        == "execution_failed"
    )