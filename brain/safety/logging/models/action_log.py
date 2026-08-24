from dataclasses import dataclass
from datetime import datetime
from typing import Any

from brain.safety.models.action import (
    Action,
)

from brain.safety.logging.models.action_log_event import (
    ActionLogEvent,
)

from brain.safety.logging.models.action_log_status import (
    ActionLogStatus,
)


@dataclass(
    frozen=True,
)
class ActionLog:
    """
    Represents one immutable event recorded
    during the lifecycle of an action.
    """

    id: str

    action: Action

    timestamp: datetime

    event: ActionLogEvent

    status: ActionLogStatus

    metadata: dict[str, Any]