from datetime import datetime, timedelta, timezone

import pytest

from brain.organization.authority_evaluation_service import (
    AuthorityEvaluationService,
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


@pytest.fixture
def organization():
    return Organization(id="madhav", name="Madhav")


@pytest.fixture
def memberships():
    return tuple(
        OrganizationMembership(
            id=f"membership-{agent_id}",
            organization_id="madhav",
            agent_id=agent_id,
            organizational_unit_id="engineering",
            role_id="developer",
            status=MembershipStatus.ACTIVE,
        )
        for agent_id in ("root", "agent-1", "agent-2", "agent-3")
    )


@pytest.fixture
def service():
    return AuthorityEvaluationService(
        trusted_authorities={"madhav": "root"}
    )


def make_grant(
    grant_id="grant-1",
    delegator="root",
    delegate="agent-1",
    *,
    actions=("read_project", "review_code"),
    targets=("project-1",),
    granted_at=NOW,
    expires_at=None,
    status=DelegationStatus.ACTIVE,
    revoked_at=None,
    parent_id=None,
    onward=False,
):
    return AuthorityDelegation(
        id=grant_id,
        organization_id="madhav",
        delegator_agent_id=delegator,
        delegate_agent_id=delegate,
        scope=DelegationScope(
            actions=actions,
            targets=targets,
        ),
        granted_at=granted_at,
        expires_at=expires_at,
        status=status,
        revoked_at=revoked_at,
        parent_delegation_id=parent_id,
        allow_onward_delegation=onward,
    )


def evaluate(
    service,
    organization,
    memberships,
    delegations,
    requester="agent-1",
    action="read_project",
    target="project-1",
    at=NOW,
):
    return service.evaluate(
        organization=organization,
        memberships=memberships,
        delegations=delegations,
        requesting_agent_id=requester,
        action=action,
        target=target,
        at=at,
    )


def test_trusted_authority_is_authorized(
    service, organization, memberships
):
    decision = evaluate(
        service,
        organization,
        memberships,
        (),
        requester="root",
        action="delete_project",
    )

    assert decision.allowed is True
    assert decision.delegation_id is None


def test_missing_trusted_authority_configuration_denies(
    organization, memberships
):
    service = AuthorityEvaluationService()

    decision = evaluate(
        service,
        organization,
        memberships,
        (),
    )

    assert decision.allowed is False
    assert "not configured" in decision.reason


def test_configuration_for_another_organization_does_not_apply(
    memberships,
):
    other_organization = Organization(
        id="other-org",
        name="Other",
    )
    service = AuthorityEvaluationService(
        trusted_authorities={"madhav": "root"}
    )

    decision = evaluate(
        service,
        other_organization,
        memberships,
        (),
    )

    assert decision.allowed is False


def test_trusted_authority_requires_active_membership(
    service, organization, memberships
):
    inactive_memberships = tuple(
        OrganizationMembership(
            id=membership.id,
            organization_id=membership.organization_id,
            agent_id=membership.agent_id,
            organizational_unit_id=membership.organizational_unit_id,
            role_id=membership.role_id,
            status=(
                MembershipStatus.INACTIVE
                if membership.agent_id == "root"
                else membership.status
            ),
        )
        for membership in memberships
    )

    decision = evaluate(
        service,
        organization,
        inactive_memberships,
        (),
        requester="root",
    )

    assert decision.allowed is False
    assert "Trusted authority lacks active" in decision.reason


def test_active_root_delegation_authorizes_in_scope_action(
    service, organization, memberships
):
    grant = make_grant()

    decision = evaluate(
        service,
        organization,
        memberships,
        (grant,),
    )

    assert decision.allowed is True
    assert decision.delegation_id == "grant-1"


def test_untrusted_agent_cannot_create_root_authority(
    service, organization, memberships
):
    grant = make_grant(delegator="agent-3")

    decision = evaluate(
        service,
        organization,
        memberships,
        (grant,),
    )

    assert decision.allowed is False
    assert "trusted authority" in decision.reason


@pytest.mark.parametrize(
    ("action", "target"),
    [
        ("delete_project", "project-1"),
        ("read_project", "project-2"),
    ],
)
def test_out_of_scope_request_is_denied(
    service,
    organization,
    memberships,
    action,
    target,
):
    decision = evaluate(
        service,
        organization,
        memberships,
        (make_grant(),),
        action=action,
        target=target,
    )

    assert decision.allowed is False


def test_expired_grant_is_denied(
    service, organization, memberships
):
    grant = make_grant(
        granted_at=NOW - timedelta(hours=1),
        expires_at=NOW,
    )

    decision = evaluate(
        service,
        organization,
        memberships,
        (grant,),
    )

    assert decision.allowed is False


def test_revoked_grant_is_denied(
    service, organization, memberships
):
    grant = make_grant(
        granted_at=NOW - timedelta(minutes=2),
        status=DelegationStatus.REVOKED,
        revoked_at=NOW - timedelta(minutes=1),
    )

    decision = evaluate(
        service,
        organization,
        memberships,
        (grant,),
    )

    assert decision.allowed is False


def test_inactive_requesting_agent_is_denied(
    service, organization, memberships
):
    inactive_memberships = tuple(
        OrganizationMembership(
            id=membership.id,
            organization_id=membership.organization_id,
            agent_id=membership.agent_id,
            organizational_unit_id=membership.organizational_unit_id,
            role_id=membership.role_id,
            status=(
                MembershipStatus.INACTIVE
                if membership.agent_id == "agent-1"
                else membership.status
            ),
        )
        for membership in memberships
    )

    decision = evaluate(
        service,
        organization,
        inactive_memberships,
        (make_grant(),),
    )

    assert decision.allowed is False


def test_parent_revocation_invalidates_child_authority(
    service, organization, memberships
):
    parent = make_grant(
        grant_id="parent",
        delegator="root",
        delegate="agent-1",
        granted_at=NOW - timedelta(hours=1),
        onward=True,
        status=DelegationStatus.REVOKED,
        revoked_at=NOW - timedelta(minutes=1),
    )

    child = make_grant(
        grant_id="child",
        delegator="agent-1",
        delegate="agent-2",
        parent_id="parent",
        actions=("read_project",),
        granted_at=NOW - timedelta(minutes=2),
    )

    decision = evaluate(
        service,
        organization,
        memberships,
        (parent, child),
        requester="agent-2",
        at=NOW,
    )

    assert decision.allowed is False


def test_child_delegation_can_authorize_with_valid_parent(
    service, organization, memberships
):
    parent = make_grant(
        grant_id="parent",
        delegate="agent-1",
        onward=True,
        expires_at=NOW + timedelta(days=2),
    )

    child = make_grant(
        grant_id="child",
        delegator="agent-1",
        delegate="agent-2",
        parent_id="parent",
        actions=("read_project",),
        granted_at=NOW + timedelta(minutes=1),
        expires_at=NOW + timedelta(days=1),
    )

    evaluation_time = NOW + timedelta(minutes=2)

    decision = evaluate(
        service,
        organization,
        memberships,
        (parent, child),
        requester="agent-2",
        at=evaluation_time,
    )

    assert decision.allowed is True
    assert decision.delegation_id == "child"


def test_multiple_matching_grants_are_ambiguous(
    service, organization, memberships
):
    first = make_grant(grant_id="grant-1")
    second = make_grant(grant_id="grant-2")

    decision = evaluate(
        service,
        organization,
        memberships,
        (first, second),
    )

    assert decision.allowed is False
    assert "ambiguous" in decision.reason


def test_duplicate_delegation_ids_fail_closed(
    service, organization, memberships
):
    first = make_grant(grant_id="duplicate")
    second = make_grant(
        grant_id="duplicate",
        delegate="agent-2",
    )

    decision = evaluate(
        service,
        organization,
        memberships,
        (first, second),
    )

    assert decision.allowed is False


def test_naive_evaluation_time_is_denied(
    service, organization, memberships
):
    decision = evaluate(
        service,
        organization,
        memberships,
        (make_grant(),),
        at=datetime(2026, 1, 1),
    )

    assert decision.allowed is False


def test_unknown_requesting_agent_is_denied(
    service, organization, memberships
):
    decision = evaluate(
        service,
        organization,
        memberships,
        (make_grant(),),
        requester="unknown-agent",
    )

    assert decision.allowed is False


def test_invalid_delegation_evidence_fails_closed(
    service, organization, memberships
):
    decision = evaluate(
        service,
        organization,
        memberships,
        (object(),),
    )

    assert decision.allowed is False
    assert "Invalid organizational evidence" in decision.reason