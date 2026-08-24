from enum import Enum


class ActionLogEvent(Enum):
    """
    Represents an event in the lifecycle
    of an action.
    """

    REQUESTED = "requested"

    EVALUATED = "evaluated"

    ALLOWED = "allowed"

    DENIED = "denied"

    APPROVAL_GRANTED = (
        "approval_granted"
    )

    APPROVAL_REJECTED = (
        "approval_rejected"
    )

    CANCELLED = "cancelled"

    EXECUTION_STARTED = (
        "execution_started"
    )

    EXECUTION_COMPLETED = (
        "execution_completed"
    )

    EXECUTION_FAILED = (
        "execution_failed"
    )