
from dataclasses import dataclass

from brain.organization.models.membership_status import MembershipStatus


@dataclass(frozen=True)
class OrganizationMembership:
    """Associates an agent with one organizational unit and role."""

    id: str
    organization_id: str
    agent_id: str
    organizational_unit_id: str
    role_id: str
    status: MembershipStatus = MembershipStatus.ACTIVE

    def __post_init__(self) -> None:
        for field_name in (
            "id",
            "organization_id",
            "agent_id",
            "organizational_unit_id",
            "role_id",
        ):
            value = getattr(self, field_name)

            if not isinstance(value, str):
                raise TypeError(f"{field_name} must be a string")

            if not value.strip():
                raise ValueError(f"{field_name} must not be empty")

        if not isinstance(self.status, MembershipStatus):
            raise TypeError("status must be a MembershipStatus")
