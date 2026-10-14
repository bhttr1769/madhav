from dataclasses import dataclass

from brain.agents.models.agent_identity import AgentIdentity
from brain.organization.models.authority_delegation import AuthorityDelegation
from brain.organization.models.organization import Organization
from brain.organization.models.organization_membership import (
    OrganizationMembership,
)
from brain.organization.models.organizational_role import OrganizationalRole
from brain.organization.models.organizational_unit import OrganizationalUnit
from brain.organization.models.reporting_relationship import (
    ReportingRelationship,
)


@dataclass(frozen=True)
class OrganizationPersistenceState:
    """Immutable snapshot of an organization's complete domain state."""

    organization: Organization
    units: tuple[OrganizationalUnit, ...]
    agents: tuple[AgentIdentity, ...]
    roles: tuple[OrganizationalRole, ...]
    memberships: tuple[OrganizationMembership, ...]
    reporting_relationships: tuple[ReportingRelationship, ...]
    delegations: tuple[AuthorityDelegation, ...] = ()

    def __post_init__(self) -> None:
        if not isinstance(self.organization, Organization):
            raise TypeError("organization must be an Organization")

        collections = (
            ("units", self.units, OrganizationalUnit),
            ("agents", self.agents, AgentIdentity),
            ("roles", self.roles, OrganizationalRole),
            ("memberships", self.memberships, OrganizationMembership),
            (
                "reporting_relationships",
                self.reporting_relationships,
                ReportingRelationship,
            ),
            ("delegations", self.delegations, AuthorityDelegation),
        )

        for field_name, items, expected_type in collections:
            if not isinstance(items, tuple):
                raise TypeError(f"{field_name} must be a tuple")

            if not all(isinstance(item, expected_type) for item in items):
                raise TypeError(
                    f"{field_name} must contain only "
                    f"{expected_type.__name__} instances"
                )