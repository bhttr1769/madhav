from enum import Enum


class DelegationStatus(Enum):
    ACTIVE = "active"
    REVOKED = "revoked"