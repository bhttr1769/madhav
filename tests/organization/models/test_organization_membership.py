
from dataclasses import FrozenInstanceError

import pytest

from brain.organization.models.membership_status import MembershipStatus
from brain.organization.models.organization_membership import (
    OrganizationMembership,
)


def test_creates_active_membership_by_default():
    membership = OrganizationMembership(
        id="membership-1",
        organization_id="madhav",
        agent_id="agent-1",
        organizational_unit_id="engineering",
        role_id="developer",
    )

    assert membership.status is MembershipStatus.ACTIVE


def test_creates_inactive_membership():
    membership = OrganizationMembership(
        id="membership-1",
        organization_id="madhav",
        agent_id="agent-1",
        organizational_unit_id="engineering",
        role_id="developer",
        status=MembershipStatus.INACTIVE,
    )

    assert membership.status is MembershipStatus.INACTIVE


@pytest.mark.parametrize(
    "field",
    [
        "id",
        "organization_id",
        "agent_id",
        "organizational_unit_id",
        "role_id",
    ],
)
@pytest.mark.parametrize("value", ["", "   "])
def test_rejects_empty_required_fields(field, value):
    values = {
        "id": "membership-1",
        "organization_id": "madhav",
        "agent_id": "agent-1",
        "organizational_unit_id": "engineering",
        "role_id": "developer",
    }
    values[field] = value

    with pytest.raises(ValueError, match=field):
        OrganizationMembership(**values)


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("id", 1),
        ("organization_id", None),
        ("agent_id", 1),
        ("organizational_unit_id", None),
        ("role_id", 1),
    ],
)
def test_rejects_invalid_required_field_types(field, value):
    values = {
        "id": "membership-1",
        "organization_id": "madhav",
        "agent_id": "agent-1",
        "organizational_unit_id": "engineering",
        "role_id": "developer",
    }
    values[field] = value

    with pytest.raises(TypeError, match=field):
        OrganizationMembership(**values)


def test_rejects_invalid_status():
    with pytest.raises(TypeError, match="status"):
        OrganizationMembership(
            id="membership-1",
            organization_id="madhav",
            agent_id="agent-1",
            organizational_unit_id="engineering",
            role_id="developer",
            status="active",
        )


def test_membership_is_immutable():
    membership = OrganizationMembership(
        "membership-1", "madhav", "agent-1", "engineering", "developer"
    )

    with pytest.raises(FrozenInstanceError):
        membership.status = MembershipStatus.INACTIVE


def test_membership_equality():
    first = OrganizationMembership(
        "membership-1", "madhav", "agent-1", "engineering", "developer"
    )
    second = OrganizationMembership(
        "membership-1", "madhav", "agent-1", "engineering", "developer"
    )

    assert first == second
