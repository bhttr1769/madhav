
from dataclasses import FrozenInstanceError

import pytest

from brain.organization.models.organizational_role import OrganizationalRole


def test_creates_role():
    role = OrganizationalRole("engineering-lead", "madhav", "Engineering Lead")

    assert role.id == "engineering-lead"
    assert role.organization_id == "madhav"
    assert role.name == "Engineering Lead"


@pytest.mark.parametrize("field", ["id", "organization_id", "name"])
@pytest.mark.parametrize("value", ["", "   "])
def test_rejects_empty_fields(field, value):
    values = {
        "id": "engineering-lead",
        "organization_id": "madhav",
        "name": "Engineering Lead",
    }
    values[field] = value

    with pytest.raises(ValueError, match=field):
        OrganizationalRole(**values)


@pytest.mark.parametrize(
    ("field", "value"),
    [("id", 1), ("organization_id", None), ("name", 1)],
)
def test_rejects_invalid_field_types(field, value):
    values = {
        "id": "engineering-lead",
        "organization_id": "madhav",
        "name": "Engineering Lead",
    }
    values[field] = value

    with pytest.raises(TypeError, match=field):
        OrganizationalRole(**values)


def test_role_is_immutable():
    role = OrganizationalRole("lead", "madhav", "Lead")

    with pytest.raises(FrozenInstanceError):
        role.name = "Director"


def test_role_equality():
    first = OrganizationalRole("lead", "madhav", "Lead")
    second = OrganizationalRole("lead", "madhav", "Lead")

    assert first == second
