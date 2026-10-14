
from collections.abc import Sequence

from brain.agents.models.agent_identity import AgentIdentity
from brain.organization.models.organization import Organization
from brain.organization.models.organizational_role import OrganizationalRole
from brain.organization.models.organization_membership import (
    OrganizationMembership,
)
from brain.organization.models.organizational_unit import OrganizationalUnit
from brain.organization.organization_structure_validator import (
    OrganizationStructureValidator,
)


class OrganizationMembershipValidator:
    """Validate membership, role, and organizational references."""

    def __init__(
        self,
        structure_validator: OrganizationStructureValidator | None = None,
    ) -> None:
        if structure_validator is not None and not isinstance(
            structure_validator, OrganizationStructureValidator
        ):
            raise TypeError(
                "structure_validator must be an "
                "OrganizationStructureValidator or None"
            )

        self._structure_validator = (
            structure_validator or OrganizationStructureValidator()
        )

    def validate(
        self,
        organization: Organization,
        units: Sequence[OrganizationalUnit],
        agents: Sequence[AgentIdentity],
        roles: Sequence[OrganizationalRole],
        memberships: Sequence[OrganizationMembership],
    ) -> None:
        if not isinstance(roles, (tuple, list)):
            raise TypeError("roles must be a tuple or list")

        if not isinstance(memberships, (tuple, list)):
            raise TypeError("memberships must be a tuple or list")

        self._structure_validator.validate(
            organization=organization,
            units=units,
            agents=agents,
            reporting_relationships=(),
        )

        unit_ids = {unit.id for unit in units}
        agent_ids = {agent.id for agent in agents}

        role_ids: set[str] = set()

        for role in roles:
            if not isinstance(role, OrganizationalRole):
                raise TypeError(
                    "roles must contain only OrganizationalRole instances"
                )

            if role.organization_id != organization.id:
                raise ValueError(
                    f"role {role.id} belongs to a different organization"
                )

            if role.id in role_ids:
                raise ValueError(f"duplicate organizational role ID: {role.id}")

            role_ids.add(role.id)

        membership_ids: set[str] = set()
        member_agent_ids: set[str] = set()

        for membership in memberships:
            if not isinstance(membership, OrganizationMembership):
                raise TypeError(
                    "memberships must contain only "
                    "OrganizationMembership instances"
                )

            if membership.id in membership_ids:
                raise ValueError(
                    f"duplicate membership ID: {membership.id}"
                )

            membership_ids.add(membership.id)

            if membership.organization_id != organization.id:
                raise ValueError(
                    f"membership {membership.id} belongs to "
                    "a different organization"
                )

            if membership.agent_id not in agent_ids:
                raise ValueError(
                    f"membership references unknown agent: "
                    f"{membership.agent_id}"
                )

            if membership.organizational_unit_id not in unit_ids:
                raise ValueError(
                    "membership references unknown organizational unit: "
                    f"{membership.organizational_unit_id}"
                )

            if membership.role_id not in role_ids:
                raise ValueError(
                    f"membership references unknown role: {membership.role_id}"
                )

            if membership.agent_id in member_agent_ids:
                raise ValueError(
                    "agent has multiple memberships in the same "
                    f"organization: {membership.agent_id}"
                )

            member_agent_ids.add(membership.agent_id)
