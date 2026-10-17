from enum import Enum


class ActionLogStatus(Enum):
    """
    Represents the state associated with
    an action log event.
    """

    PENDING = "pending"

    ALLOWED = "allowed"

    DENIED = "denied"

    WAITING_APPROVAL = (
        "waiting_approval"
    )

    RUNNING = "running"

    COMPLETED = "completed"

    FAILED = "failed"
  
    UNCERTAIN = "uncertain"