from dataclasses import FrozenInstanceError
from datetime import datetime, timedelta, timezone

import pytest

from brain.organization.models.authority_delegation import AuthorityDelegation
from brain.organization.models.delegation_scope import DelegationScope
from brain.organization.models.delegation_status import DelegationStatus


NOW = datetime(2026, 1, 1, tzinfo=timezone.utc)


def make_delegation(**overrides):
    values = {
        "id": "grant-1",
        "organization_id": "madhav",
        "delegator_agent_id": "agent-1",
        "delegate_agent_id": "agent-2",
        "scope": DelegationScope(
            actions=("read_project", "review_code"),
            targets=("project-1",),
        ),
        "granted_at": NOW,
    }
    values.update(overrides)
    return AuthorityDelegation(**values)


def test_creates_active_delegation_by_default():
    grant = make_delegation()

    assert grant.status is DelegationStatus.ACTIVE
    assert grant.allow_onward_delegation is False
    assert grant.parent_delegation_id is None


def test_delegation_is_immutable():
    grant = make_delegation()

    with pytest.raises(FrozenInstanceError):
        grant.status = DelegationStatus.REVOKED


def test_rejects_self_delegation():
    with pytest.raises(ValueError, match="itself"):
        make_delegation(delegate_agent_id="agent-1")


def test_rejects_empty_required_identifier():
    with pytest.raises(ValueError, match="organization_id"):
        make_delegation(organization_id=" ")


def test_rejects_invalid_scope_type():
    with pytest.raises(TypeError, match="scope"):
        make_delegation(scope=None)


def test_rejects_naive_grant_time():
    with pytest.raises(ValueError, match="timezone-aware"):
        make_delegation(granted_at=datetime(2026, 1, 1))


def test_rejects_expiry_before_or_at_grant_time():
    with pytest.raises(ValueError, match="after granted_at"):
        make_delegation(expires_at=NOW)


def test_rejects_revoked_status_without_timestamp():
    with pytest.raises(ValueError, match="must have revoked_at"):
        make_delegation(status=DelegationStatus.REVOKED)


def test_rejects_revocation_timestamp_on_active_grant():
    with pytest.raises(ValueError, match="cannot have revoked_at"):
        make_delegation(revoked_at=NOW + timedelta(minutes=1))


def test_is_effective_before_expiry():
    grant = make_delegation(expires_at=NOW + timedelta(hours=1))

    assert grant.is_effective_at(NOW)
    assert grant.is_effective_at(NOW + timedelta(minutes=59))


def test_is_not_effective_at_or_after_expiry():
    expiry = NOW + timedelta(hours=1)
    grant = make_delegation(expires_at=expiry)

    assert not grant.is_effective_at(expiry)
    assert not grant.is_effective_at(expiry + timedelta(seconds=1))


def test_revoked_grant_is_not_effective():
    grant = make_delegation(
        status=DelegationStatus.REVOKED,
        revoked_at=NOW + timedelta(minutes=1),
    )

    assert not grant.is_effective_at(NOW + timedelta(minutes=2))


def test_rejects_empty_scope():
    with pytest.raises(ValueError, match="actions"):
        DelegationScope(actions=(), targets=("project-1",))


def test_rejects_wildcard_scope():
    with pytest.raises(ValueError, match="explicit values"):
        DelegationScope(actions=("*",), targets=("project-1",))


def test_rejects_duplicate_scope_entries():
    with pytest.raises(ValueError, match="duplicates"):
        DelegationScope(
            actions=("read_project", "read_project"),
            targets=("project-1",),
        )