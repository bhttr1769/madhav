from brain.safety.logging.models.action_log_status import (
    ActionLogStatus,
)


def test_action_log_status_values():

    assert (
        ActionLogStatus.PENDING.value
        == "pending"
    )

    assert (
        ActionLogStatus.ALLOWED.value
        == "allowed"
    )

    assert (
        ActionLogStatus.DENIED.value
        == "denied"
    )

    assert (
        ActionLogStatus.WAITING_APPROVAL.value
        == "waiting_approval"
    )

    assert (
        ActionLogStatus.RUNNING.value
        == "running"
    )

    assert (
        ActionLogStatus.COMPLETED.value
        == "completed"
    )

    assert (
        ActionLogStatus.FAILED.value
        == "failed"
    )