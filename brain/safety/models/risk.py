from enum import Enum


class Risk(Enum):
    """
    Represents the potential impact of an action.
    """

    SAFE = 0

    LOW = 1

    MEDIUM = 2

    HIGH = 3

    CRITICAL = 4