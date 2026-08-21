from dataclasses import dataclass

from brain.safety.models.action import (
    Action,
)

from brain.safety.models.risk import (
    Risk,
)


@dataclass(
    frozen=True,
)
class ApprovalRequest:
    """
    Represents an action awaiting user approval.
    """

    action: Action

    risk: Risk