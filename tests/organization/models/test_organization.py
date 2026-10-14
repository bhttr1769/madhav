
from dataclasses import FrozenInstanceError

import pytest

from brain.organization.models.organization import Organization


def test_creates_organization():
    organization = Organization("madhav", "Madhav AI")

    assert organization.id == "madhav"
    assert organization.name == "Madhav AI"


@pytest.mark.parametrize("field", ["id", "name"])
@pytest.mark.parametrize("value", ["", "   "])
def test_rejects_empty_required_fields(field, value):
    values = {"id": "madhav", "name": "Madhav AI"}
    values[field] = value

    with pytest.raises(ValueError, match=field):
        Organization(**values)


@pytest.mark.parametrize(
    ("field", "value"),
    [("id", 123), ("name", None)],
)
def test_rejects_invalid_field_types(field, value):
    values = {"id": "madhav", "name": "Madhav AI"}
    values[field] = value

    with pytest.raises(TypeError, match=field):
        Organization(**values)


def test_organization_is_immutable():
    organization = Organization("madhav", "Madhav AI")

    with pytest.raises(FrozenInstanceError):
        organization.name = "Changed"


def test_organization_equality():
    first = Organization("madhav", "Madhav AI")
    second = Organization("madhav", "Madhav AI")

    assert first == second
