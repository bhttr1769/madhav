from brain.safety.logging.models.action_log_event import (
    ActionLogEvent,
)


def test_action_log_event_values():

    expected = {
        "requested",
        "evaluated",
        "allowed",
        "denied",
        "approval_granted",
        "approval_rejected",
        "cancelled",
        "execution_started",
        "execution_completed",
        "execution_failed",
    }

    actual = {
        event.value
        for event in ActionLogEvent
    }

    assert actual == expected