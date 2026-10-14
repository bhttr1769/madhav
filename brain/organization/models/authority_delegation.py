from dataclasses import dataclass
from datetime import datetime

from brain.organization.models.delegation_scope import DelegationScope
from brain.organization.models.delegation_status import DelegationStatus


def _require_aware_datetime(value: datetime, field_name: str) -> None:
    if not isinstance(value, datetime):
        raise TypeError(f"{field_name} must be a datetime")

    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError(f"{field_name} must be timezone-aware")


@dataclass(frozen=True)
class AuthorityDelegation:
    """An explicit, bounded grant of authority between organizational agents."""

    id: str
    organization_id: str
    delegator_agent_id: str
    delegate_agent_id: str
    scope: DelegationScope
    granted_at: datetime
    expires_at: datetime | None = None
    status: DelegationStatus = DelegationStatus.ACTIVE
    revoked_at: datetime | None = None
    parent_delegation_id: str | None = None
    allow_onward_delegation: bool = False

    def __post_init__(self) -> None:
        for field_name in (
            "id",
            "organization_id",
            "delegator_agent_id",
            "delegate_agent_id",
        ):
            value = getattr(self, field_name)

            if not isinstance(value, str):
                raise TypeError(f"{field_name} must be a string")

            if not value.strip():
                raise ValueError(f"{field_name} must not be empty")

        if self.delegator_agent_id == self.delegate_agent_id:
            raise ValueError("an agent cannot delegate authority to itself")

        if not isinstance(self.scope, DelegationScope):
            raise TypeError("scope must be a DelegationScope")

        if not isinstance(self.status, DelegationStatus):
            raise TypeError("status must be a DelegationStatus")

        if not isinstance(self.allow_onward_delegation, bool):
            raise TypeError("allow_onward_delegation must be a boolean")

        _require_aware_datetime(self.granted_at, "granted_at")

        if self.expires_at is not None:
            _require_aware_datetime(self.expires_at, "expires_at")

            if self.expires_at <= self.granted_at:
                raise ValueError("expires_at must be after granted_at")

        if self.revoked_at is not None:
            _require_aware_datetime(self.revoked_at, "revoked_at")

            if self.revoked_at < self.granted_at:
                raise ValueError("revoked_at cannot precede granted_at")

        if self.status is DelegationStatus.ACTIVE:
            if self.revoked_at is not None:
                raise ValueError(
                    "an active delegation cannot have revoked_at"
                )

        if self.status is DelegationStatus.REVOKED:
            if self.revoked_at is None:
                raise ValueError(
                    "a revoked delegation must have revoked_at"
                )

        if self.parent_delegation_id is not None:
            if not isinstance(self.parent_delegation_id, str):
                raise TypeError("parent_delegation_id must be a string or None")

            if not self.parent_delegation_id.strip():
                raise ValueError("parent_delegation_id must not be empty")

            if self.parent_delegation_id == self.id:
                raise ValueError("a delegation cannot be its own parent")

    def is_effective_at(self, moment: datetime) -> bool:
        """Return whether this grant is effective at a given instant."""
        _require_aware_datetime(moment, "moment")

        if self.status is not DelegationStatus.ACTIVE:
            return False

        if moment < self.granted_at:
            return False

        if self.expires_at is not None and moment >= self.expires_at:
            return False

        return True