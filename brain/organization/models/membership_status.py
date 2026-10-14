
from enum import Enum


class MembershipStatus(Enum):
    """Lifecycle status of an agent's organizational membership."""

    ACTIVE = "active"
    INACTIVE = "inactive"
