from collections.abc import Mapping, Sequence
from datetime import datetime

from brain.organization.authority_delegation_validator import (
    AuthorityDelegationValidator,
)
from brain.organization.models.authority_decision import AuthorityDecision
from brain.organization.models.authority_delegation import AuthorityDelegation
from brain.organization.models.delegation_status import DelegationStatus
from brain.organization.models.membership_status import MembershipStatus
from brain.organization.models.organization import Organization
from brain.organization.models.organization_membership import (
    OrganizationMembership,
)


class AuthorityEvaluationService:
    """
    Evaluate organizational authority independently of safety permissions.

    Each organization must have an explicitly configured trusted authority.
    Delegated authority must originate from that authority through a valid
    chain of delegations.

    Reporting relationships do not automatically grant action authority.
    """

    def __init__(
        self,
        trusted_authorities: Mapping[str, str] | None = None,
        delegation_validator: AuthorityDelegationValidator | None = None,
    ) -> None:
        if trusted_authorities is not None:
            if not isinstance(trusted_authorities, Mapping):
                raise TypeError(
                    "trusted_authorities must be a mapping or None"
                )

            for organization_id, agent_id in trusted_authorities.items():
                if not isinstance(organization_id, str):
                    raise TypeError(
                        "trusted authority organization IDs must be strings"
                    )

                if not organization_id.strip():
                    raise ValueError(
                        "trusted authority organization IDs must not be empty"
                    )

                if not isinstance(agent_id, str):
                    raise TypeError(
                        "trusted authority agent IDs must be strings"
                    )

                if not agent_id.strip():
                    raise ValueError(
                        "trusted authority agent IDs must not be empty"
                    )

        if delegation_validator is not None and not isinstance(
            delegation_validator, AuthorityDelegationValidator
        ):
            raise TypeError(
                "delegation_validator must be an "
                "AuthorityDelegationValidator or None"
            )

        # Copy configuration so later caller-side mapping changes do not
        # silently change this service's trust configuration.
        self._trusted_authorities = dict(trusted_authorities or {})
        self._delegation_validator = (
            delegation_validator or AuthorityDelegationValidator()
        )

    def evaluate(
        self,
        organization: Organization,
        memberships: Sequence[OrganizationMembership],
        delegations: Sequence[AuthorityDelegation],
        requesting_agent_id: str,
        action: str,
        target: str,
        at: datetime,
    ) -> AuthorityDecision:
        """
        Evaluate authority for one action and target at a specific instant.

        Invalid or ambiguous evidence produces a denial. This service does
        not replace Madhav's separate safety permission or execution checks.
        """

        if not isinstance(organization, Organization):
            return self._deny("Invalid organization.")

        trusted_id = self._trusted_authorities.get(organization.id)

        if trusted_id is None:
            return self._deny(
                "Trusted authority is not configured for this organization."
            )

        if not isinstance(requesting_agent_id, str):
            return self._deny("Invalid requesting agent.")

        if not requesting_agent_id.strip():
            return self._deny("Invalid requesting agent.")

        if not isinstance(action, str) or not action.strip():
            return self._deny("Invalid action.")

        if not isinstance(target, str) or not target.strip():
            return self._deny("Invalid target.")

        if not isinstance(at, datetime):
            return self._deny("Invalid evaluation time.")

        if at.tzinfo is None or at.utcoffset() is None:
            return self._deny(
                "Evaluation time must be timezone-aware."
            )

        if not self._is_sequence(memberships):
            return self._deny("Invalid membership data.")

        if not self._is_sequence(delegations):
            return self._deny("Invalid delegation data.")

        try:
            active_agent_ids = self._validate_memberships(
                organization=organization,
                memberships=memberships,
            )

            delegation_by_id = self._index_delegations(
                organization=organization,
                delegations=delegations,
            )
        except (TypeError, ValueError) as exc:
            return self._deny(
                f"Invalid organizational evidence: {exc}"
            )

        if trusted_id not in active_agent_ids:
            return self._deny(
                "Trusted authority lacks active organizational membership."
            )

        if requesting_agent_id not in active_agent_ids:
            return self._deny(
                "Requesting agent lacks active organizational membership."
            )

        # This grants organizational authority to the configured root only.
        # Safety policy evaluation and execution authorization remain separate.
        if requesting_agent_id == trusted_id:
            return AuthorityDecision(
                allowed=True,
                reason=(
                    "Requesting agent is the trusted organizational authority."
                ),
            )

        matching_delegations = [
            delegation
            for delegation in delegation_by_id.values()
            if (
                delegation.delegate_agent_id == requesting_agent_id
                and delegation.status is DelegationStatus.ACTIVE
                and delegation.is_effective_at(at)
                and action in delegation.scope.actions
                and target in delegation.scope.targets
            )
        ]

        if not matching_delegations:
            return self._deny(
                "No effective delegation covers the requested action and target."
            )

        if len(matching_delegations) != 1:
            return self._deny(
                "Multiple matching delegations make authority ambiguous."
            )

        candidate = matching_delegations[0]

        try:
            chain = self._resolve_chain(
                candidate=candidate,
                delegations_by_id=delegation_by_id,
                at=at,
            )

            chain_agent_ids = {
                agent_id
                for grant in chain
                for agent_id in (
                    grant.delegator_agent_id,
                    grant.delegate_agent_id,
                )
            }

            if not chain_agent_ids.issubset(active_agent_ids):
                return self._deny(
                    "A delegation-chain agent lacks active membership."
                )

            chain_memberships = tuple(
                membership
                for membership in memberships
                if membership.agent_id in chain_agent_ids
            )

            # Reuse the existing validator instead of duplicating the
            # delegation-chain structural and scope rules.
            self._delegation_validator.validate(
                organization=organization,
                memberships=chain_memberships,
                delegations=chain,
            )

        except (TypeError, ValueError, KeyError) as exc:
            return self._deny(
                f"Delegation chain is invalid: {exc}"
            )

        # _resolve_chain returns the candidate first and root last.
        root_delegation = chain[-1]

        if root_delegation.delegator_agent_id != trusted_id:
            return self._deny(
                "Delegation chain does not originate from trusted authority."
            )

        return AuthorityDecision(
            allowed=True,
            reason=(
                "A valid delegation covers the requested action and target."
            ),
            delegation_id=candidate.id,
        )

    @staticmethod
    def _is_sequence(value: object) -> bool:
        return isinstance(value, (tuple, list))

    @staticmethod
    def _validate_memberships(
        organization: Organization,
        memberships: Sequence[OrganizationMembership],
    ) -> set[str]:
        active_agent_ids: set[str] = set()
        seen_agent_ids: set[str] = set()
        seen_membership_ids: set[str] = set()

        for membership in memberships:
            if not isinstance(membership, OrganizationMembership):
                raise TypeError(
                    "memberships must contain OrganizationMembership objects"
                )

            if membership.organization_id != organization.id:
                raise ValueError(
                    "membership belongs to a different organization"
                )

            if membership.id in seen_membership_ids:
                raise ValueError(
                    f"duplicate membership ID: {membership.id}"
                )

            if membership.agent_id in seen_agent_ids:
                raise ValueError(
                    "agent has multiple memberships in the organization: "
                    f"{membership.agent_id}"
                )

            seen_membership_ids.add(membership.id)
            seen_agent_ids.add(membership.agent_id)

            if membership.status is MembershipStatus.ACTIVE:
                active_agent_ids.add(membership.agent_id)

        return active_agent_ids

    @staticmethod
    def _index_delegations(
        organization: Organization,
        delegations: Sequence[AuthorityDelegation],
    ) -> dict[str, AuthorityDelegation]:
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

            by_id[delegation.id] = delegation

        return by_id

    @staticmethod
    def _resolve_chain(
        candidate: AuthorityDelegation,
        delegations_by_id: dict[str, AuthorityDelegation],
        at: datetime,
    ) -> tuple[AuthorityDelegation, ...]:
        """Return the delegation chain from candidate back to its root."""

        chain: list[AuthorityDelegation] = []
        visited: set[str] = set()
        current = candidate

        while True:
            if current.id in visited:
                raise ValueError(
                    "delegation chain contains a cycle"
                )

            visited.add(current.id)
            chain.append(current)

            # Checking every ancestor at evaluation time means a revoked
            # or expired parent invalidates all authority inherited from it.
            if not current.is_effective_at(at):
                raise ValueError(
                    "delegation is expired, revoked, or not yet valid: "
                    f"{current.id}"
                )

            if current.parent_delegation_id is None:
                break

            parent = delegations_by_id.get(
                current.parent_delegation_id
            )

            if parent is None:
                raise ValueError(
                    "parent delegation does not exist: "
                    f"{current.parent_delegation_id}"
                )

            current = parent

        return tuple(chain)

    @staticmethod
    def _deny(reason: str) -> AuthorityDecision:
        return AuthorityDecision(
            allowed=False,
            reason=reason,
        )