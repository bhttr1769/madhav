from collections.abc import Sequence

from brain.agents.models.agent_identity import AgentIdentity
from brain.organization.models.membership_status import MembershipStatus
from brain.organization.models.organization import Organization
from brain.organization.models.organization_membership import (
    OrganizationMembership,
)
from brain.organization.models.organizational_role import OrganizationalRole
from brain.organization.models.organizational_unit import OrganizationalUnit
from brain.organization.models.reporting_relationship import (
    ReportingRelationship,
)
from brain.organization.organization_membership_validator import (
    OrganizationMembershipValidator,
)
from brain.organization.organization_structure_validator import (
    OrganizationStructureValidator,
)


class OrganizationIntegrityValidator:
    """Validate the consistency of a complete organization snapshot."""

    def __init__(
        self,
        structure_validator: OrganizationStructureValidator | None = None,
        membership_validator: OrganizationMembershipValidator | None = None,
    ) -> None:
        if structure_validator is not None and not isinstance(
            structure_validator, OrganizationStructureValidator
        ):
            raise TypeError(
                "structure_validator must be an "
                "OrganizationStructureValidator or None"
            )

        if membership_validator is not None and not isinstance(
            membership_validator, OrganizationMembershipValidator
        ):
            raise TypeError(
                "membership_validator must be an "
                "OrganizationMembershipValidator or None"
            )

        self._structure_validator = (
            structure_validator or OrganizationStructureValidator()
        )
        self._membership_validator = (
            membership_validator or OrganizationMembershipValidator()
        )

    def validate(
        self,
        organization: Organization,
        units: Sequence[OrganizationalUnit],
        agents: Sequence[AgentIdentity],
        roles: Sequence[OrganizationalRole],
        memberships: Sequence[OrganizationMembership],
        reporting_relationships: Sequence[ReportingRelationship],
    ) -> None:
        """Raise an exception if any organizational invariant is violated."""

        # Validate the reporting hierarchy, including references and cycles.
        self._structure_validator.validate(
            organization=organization,
            units=units,
            agents=agents,
            reporting_relationships=reporting_relationships,
        )

        # Reuse existing membership, role, and reference validation.
        self._membership_validator.validate(
            organization=organization,
            units=units,
            agents=agents,
            roles=roles,
            memberships=memberships,
        )

        active_member_ids = {
            membership.agent_id
            for membership in memberships
            if membership.status is MembershipStatus.ACTIVE
        }

        for relationship in reporting_relationships:
            if relationship.agent_id not in active_member_ids:
                raise ValueError(
                    "reporting agent must have an active organizational "
                    f"membership: {relationship.agent_id}"
                )

            if relationship.manager_agent_id not in active_member_ids:
                raise ValueError(
                    "manager agent must have an active organizational "
                    f"membership: {relationship.manager_agent_id}"
                )
