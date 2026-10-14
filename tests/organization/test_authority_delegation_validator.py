from datetime import datetime, timedelta, timezone

import pytest

from brain.agents.models.agent_identity import AgentIdentity
from brain.organization.authority_delegation_validator import (
    AuthorityDelegationValidator,
)
from brain.organization.models.authority_delegation import AuthorityDelegation
from brain.organization.models.delegation_scope import DelegationScope
from brain.organization.models.delegation_status import DelegationStatus
from brain.organization.models.membership_status import MembershipStatus
from brain.organization.models.organization import Organization
from brain.organization.models.organization_membership import (
    OrganizationMembership,
)


NOW = datetime(2026, 1, 1, tzinfo=timezone.utc)


def make_membership(agent_id, status=MembershipStatus.ACTIVE):
    return OrganizationMembership(
        id=f"membership-{agent_id}",
        organization_id="madhav",
        agent_id=agent_id,
        organizational_unit_id="engineering",
        role_id="developer",
        status=status,
    )


def make_delegation(**overrides):
    values = {
        "id": "grant-1",
        "organization_id": "madhav",
        "delegator_agent_id": "agent-1",
        "delegate_agent_id": "agent-2",
        "scope": DelegationScope(
            actions=("read_project", "review_code"),
            targets=("project-1", "project-2"),
        ),
        "granted_at": NOW,
    }
    values.update(overrides)
    return AuthorityDelegation(**values)


@pytest.fixture
def organization():
    return Organization(id="madhav", name="Madhav")


@pytest.fixture
def memberships():
    return (
        make_membership("agent-1"),
        make_membership("agent-2"),
        make_membership("agent-3"),
    )


@pytest.fixture
def validator():
    return AuthorityDelegationValidator()


def test_accepts_valid_delegation(
    validator, organization, memberships
):
    validator.validate(
        organization,
        memberships,
        (make_delegation(),),
    )


def test_rejects_delegator_without_active_membership(
    validator, organization
):
    with pytest.raises(ValueError, match="delegator must have an active"):
        validator.validate(
            organization,
            (make_membership("agent-2"),),
            (make_delegation(),),
        )


def test_rejects_delegate_with_inactive_membership(
    validator, organization
):
    memberships = (
        make_membership("agent-1"),
        make_membership("agent-2", MembershipStatus.INACTIVE),
    )

    with pytest.raises(ValueError, match="delegate must have an active"):
        validator.validate(
            organization,
            memberships,
            (make_delegation(),),
        )


def test_rejects_delegation_for_another_organization(
    validator, organization, memberships
):
    with pytest.raises(ValueError, match="different organization"):
        validator.validate(
            organization,
            memberships,
            (make_delegation(organization_id="other-org"),),
        )


def test_rejects_duplicate_delegation_ids(
    validator, organization, memberships
):
    first = make_delegation()
    second = make_delegation(delegate_agent_id="agent-3")

    with pytest.raises(ValueError, match="duplicate delegation ID"):
        validator.validate(
            organization,
            memberships,
            (first, second),
        )


def test_rejects_missing_parent(
    validator, organization, memberships
):
    child = make_delegation(
        parent_delegation_id="missing",
    )

    with pytest.raises(ValueError, match="does not exist"):
        validator.validate(organization, memberships, (child,))


def test_rejects_onward_delegation_without_permission(
    validator, organization, memberships
):
    parent = make_delegation(
        allow_onward_delegation=False,
    )
    child = make_delegation(
        id="grant-2",
        delegator_agent_id="agent-2",
        delegate_agent_id="agent-3",
        parent_delegation_id="grant-1",
    )

    with pytest.raises(ValueError, match="does not permit onward"):
        validator.validate(
            organization,
            memberships,
            (parent, child),
        )


def test_accepts_bounded_onward_delegation(
    validator, organization, memberships
):
    parent = make_delegation(
        expires_at=NOW + timedelta(days=2),
        allow_onward_delegation=True,
    )
    child = make_delegation(
        id="grant-2",
        delegator_agent_id="agent-2",
        delegate_agent_id="agent-3",
        parent_delegation_id="grant-1",
        scope=DelegationScope(
            actions=("read_project",),
            targets=("project-1",),
        ),
        granted_at=NOW + timedelta(minutes=1),
        expires_at=NOW + timedelta(days=1),
    )

    validator.validate(
        organization,
        memberships,
        (parent, child),
    )


def test_rejects_child_scope_expansion(
    validator, organization, memberships
):
    parent = make_delegation(allow_onward_delegation=True)
    child = make_delegation(
        id="grant-2",
        delegator_agent_id="agent-2",
        delegate_agent_id="agent-3",
        parent_delegation_id="grant-1",
        scope=DelegationScope(
            actions=("delete_project",),
            targets=("project-1",),
        ),
    )

    with pytest.raises(ValueError, match="actions exceed parent scope"):
        validator.validate(
            organization,
            memberships,
            (parent, child),
        )


def test_rejects_child_that_outlives_parent(
    validator, organization, memberships
):
    parent = make_delegation(
        expires_at=NOW + timedelta(days=1),
        allow_onward_delegation=True,
    )
    child = make_delegation(
        id="grant-2",
        delegator_agent_id="agent-2",
        delegate_agent_id="agent-3",
        parent_delegation_id="grant-1",
        expires_at=NOW + timedelta(days=2),
    )

    with pytest.raises(ValueError, match="cannot outlive its parent"):
        validator.validate(
            organization,
            memberships,
            (parent, child),
        )


def test_rejects_child_created_after_parent_revocation(
    validator, organization, memberships
):
    parent = make_delegation(
        allow_onward_delegation=True,
        status=DelegationStatus.REVOKED,
        revoked_at=NOW + timedelta(minutes=1),
    )
    child = make_delegation(
        id="grant-2",
        delegator_agent_id="agent-2",
        delegate_agent_id="agent-3",
        parent_delegation_id="grant-1",
        granted_at=NOW + timedelta(minutes=2),
    )

    with pytest.raises(ValueError, match="already revoked"):
        validator.validate(
            organization,
            memberships,
            (parent, child),
        )