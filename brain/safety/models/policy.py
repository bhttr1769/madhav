from dataclasses import dataclass

from brain.safety.models.risk import (
    Risk,
)

from brain.safety.models.permission_decision import (
    PermissionDecision,
)


@dataclass(
    frozen=True,
)
class Policy:
    """
    Defines how actions within a category are evaluated.
    """

    category: str

    maximum_risk: Risk

    decision: PermissionDecision