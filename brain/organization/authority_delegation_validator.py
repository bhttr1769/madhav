from collections.abc import Sequence

from brain.organization.models.authority_delegation import AuthorityDelegation
from brain.organization.models.delegation_status import DelegationStatus
from brain.organization.models.organization import Organization
from brain.organization.models.organization_membership import (
    OrganizationMembership,
)
from brain.organization.models.membership_status import MembershipStatus


class AuthorityDelegationValidator:
    """Validate delegation records against organizational membership and limits."""

    def validate(
        self,
        organization: Organization,
        memberships: Sequence[OrganizationMembership],
        delegations: Sequence[AuthorityDelegation],
    ) -> None:
        if not isinstance(organization, Organization):
            raise TypeError("organization must be an Organization")

        if not isinstance(memberships, Sequence) or isinstance(
            memberships, (str, bytes)
        ):
            raise TypeError("memberships must be a sequence")

        if not isinstance(delegations, Sequence) or isinstance(
            delegations, (str, bytes)
        ):
            raise TypeError("delegations must be a sequence")

        active_agents: set[str] = set()

        for membership in memberships:
            if not isinstance(membership, OrganizationMembership):
                raise TypeError(
                    "memberships must contain OrganizationMembership objects"
                )

            if membership.organization_id != organization.id:
                raise ValueError(
                    "membership belongs to a different organization"
                )

            if membership.status is MembershipStatus.ACTIVE:
                if membership.agent_id in active_agents:
                    raise ValueError(
                        "an agent cannot have duplicate active memberships "
                        "in the same organization"
                    )

                active_agents.add(membership.agent_id)

        by_id: dict[str, AuthorityDelegation] = {}

        for delegation in delegations:
            if not isinstance(delegation, AuthorityDelegation):
                raise TypeError(
                    "delegations must contain AuthorityDelegation objects"
                )

            if delegation.organization_id != organization.id:
                raise ValueError(
                    "delegation belongs to a different organization"
                )

            if delegation.id in by_id:
                raise ValueError(
                    f"duplicate delegation ID: {delegation.id}"
                )

            if delegation.delegator_agent_id not in active_agents:
                raise ValueError(
                    "delegator must have an active organizational "
                    f"membership: {delegation.delegator_agent_id}"
                )

            if delegation.delegate_agent_id not in active_agents:
                raise ValueError(
                    "delegate must have an active organizational "
                    f"membership: {delegation.delegate_agent_id}"
                )

            by_id[delegation.id] = delegation

        for delegation in delegations:
            if delegation.parent_delegation_id is not None:
                self._validate_parent(delegation, by_id)

        self._validate_acyclic_chains(by_id)

    @staticmethod
    def _validate_parent(
        delegation: AuthorityDelegation,
        delegations_by_id: dict[str, AuthorityDelegation],
    ) -> None:
        parent = delegations_by_id.get(delegation.parent_delegation_id)

        if parent is None:
            raise ValueError(
                "parent delegation does not exist: "
                f"{delegation.parent_delegation_id}"
            )

        if parent.organization_id != delegation.organization_id:
            raise ValueError(
                "parent delegation must belong to the same organization"
            )

        if parent.delegate_agent_id != delegation.delegator_agent_id:
            raise ValueError(
                "parent delegate must match child delegator"
            )

        if not parent.allow_onward_delegation:
            raise ValueError(
                "parent delegation does not permit onward delegation"
            )

        if delegation.granted_at < parent.granted_at:
            raise ValueError(
                "child delegation cannot precede its parent grant"
            )

        if (
            parent.revoked_at is not None
            and parent.revoked_at <= delegation.granted_at
        ):
            raise ValueError(
                "cannot create a child delegation from an already revoked grant"
            )

        if (
            parent.expires_at is not None
            and delegation.granted_at >= parent.expires_at
        ):
            raise ValueError(
                "cannot create a child delegation after parent expiry"
            )

        if not set(delegation.scope.actions).issubset(
            parent.scope.actions
        ):
            raise ValueError(
                "child delegation actions exceed parent scope"
            )

        if not set(delegation.scope.targets).issubset(
            parent.scope.targets
        ):
            raise ValueError(
                "child delegation targets exceed parent scope"
            )

        if parent.expires_at is not None:
            if (
                delegation.expires_at is None
                or delegation.expires_at > parent.expires_at
            ):
                raise ValueError(
                    "child delegation cannot outlive its parent"
                )

    @staticmethod
    def _validate_acyclic_chains(
        delegations_by_id: dict[str, AuthorityDelegation],
    ) -> None:
        for delegation in delegations_by_id.values():
            visited: set[str] = set()
            current = delegation

            while current.parent_delegation_id is not None:
                if current.id in visited:
                    raise ValueError("delegation chain contains a cycle")

                visited.add(current.id)

                parent = delegations_by_id.get(
                    current.parent_delegation_id
                )

                if parent is None:
                    # Missing parents are rejected by _validate_parent.
                    break

                current = parent

            if current.id in visited:
                raise ValueError("delegation chain contains a cycle")