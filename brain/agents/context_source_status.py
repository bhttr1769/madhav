from enum import Enum


class ContextSourceStatus(str, Enum):
    AVAILABLE = "available"
    UNAVAILABLE = "unavailable"
    EMPTY = "empty"
    FAILED = "failed"
    NOT_REQUESTED = "not_requested"