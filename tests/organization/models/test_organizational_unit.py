
from dataclasses import FrozenInstanceError

import pytest

from brain.organization.models.organizational_unit import OrganizationalUnit


def test_creates_root_unit():
    unit = OrganizationalUnit(
        id="engineering",
        organization_id="madhav",
        name="Engineering",
    )

    assert unit.parent_unit_id is None


def test_creates_child_unit():
    unit = OrganizationalUnit(
        id="backend",
        organization_id="madhav",
        name="Backend",
        parent_unit_id="engineering",
    )

    assert unit.parent_unit_id == "engineering"


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("id", ""),
        ("organization_id", ""),
        ("name", ""),
        ("id", "   "),
        ("organization_id", "   "),
        ("name", "   "),
    ],
)
def test_rejects_empty_required_fields(field, value):
    values = {
        "id": "engineering",
        "organization_id": "madhav",
        "name": "Engineering",
    }
    values[field] = value

    with pytest.raises(ValueError, match=field):
        OrganizationalUnit(**values)


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("id", 1),
        ("organization_id", None),
        ("name", 1),
    ],
)
def test_rejects_invalid_required_field_types(field, value):
    values = {
        "id": "engineering",
        "organization_id": "madhav",
        "name": "Engineering",
    }
    values[field] = value

    with pytest.raises(TypeError, match=field):
        OrganizationalUnit(**values)


def test_rejects_empty_parent_id():
    with pytest.raises(ValueError, match="parent_unit_id"):
        OrganizationalUnit(
            id="engineering",
            organization_id="madhav",
            name="Engineering",
            parent_unit_id=" ",
        )


def test_rejects_non_string_parent_id():
    with pytest.raises(TypeError, match="parent_unit_id"):
        OrganizationalUnit(
            id="engineering",
            organization_id="madhav",
            name="Engineering",
            parent_unit_id=123,
        )


def test_rejects_self_parent():
    with pytest.raises(ValueError, match="own parent"):
        OrganizationalUnit(
            id="engineering",
            organization_id="madhav",
            name="Engineering",
            parent_unit_id="engineering",
        )


def test_unit_is_immutable():
    unit = OrganizationalUnit(
        id="engineering",
        organization_id="madhav",
        name="Engineering",
    )

    with pytest.raises(FrozenInstanceError):
        unit.name = "Research"


def test_unit_equality():
    first = OrganizationalUnit("engineering", "madhav", "Engineering")
    second = OrganizationalUnit("engineering", "madhav", "Engineering")

    assert first == second
