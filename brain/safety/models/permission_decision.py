from enum import Enum


class PermissionDecision(Enum):
    """
    Represents the result of permission evaluation.
    """

    ALLOW = "allow"

    DENY = "deny"

    ASK = "ask"