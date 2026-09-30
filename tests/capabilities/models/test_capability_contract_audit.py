from dataclasses import fields, is_dataclass

import pytest

from brain.capabilities.models.capability_descriptor import (
    CapabilityDescriptor,
)


def create_capability_descriptor() -> CapabilityDescriptor:
    return CapabilityDescriptor(
        id="test.capability",
        name="Test Capability",
        description="Capability used for contract auditing.",
        version="1.0.0",
        entry_point=(
            "tests.capabilities.models."
            "test_capability_contract_audit.TestCapability"
        ),
        dependencies=frozenset(
            {
                "dependency.one",
                "dependency.two",
            }
        ),
    )


class TestCapability:
    def execute(
        self,
        input_data: object,
    ) -> object:
        return input_data


def test_capability_descriptor_is_dataclass() -> None:
    assert is_dataclass(CapabilityDescriptor)


def test_capability_descriptor_is_frozen() -> None:
    descriptor = create_capability_descriptor()

    with pytest.raises(
        AttributeError,
    ):
        descriptor.id = "changed"


def test_capability_descriptor_has_current_contract_fields() -> None:
    descriptor_fields = tuple(
        field.name
        for field in fields(CapabilityDescriptor)
    )

    assert descriptor_fields == (
        "id",
        "name",
        "description",
        "version",
        "entry_point",
        "dependencies",
        "input_contract",
        "output_contract",
    )


def test_capability_descriptor_stores_identity_fields() -> None:
    descriptor = create_capability_descriptor()

    assert descriptor.id == "test.capability"
    assert descriptor.name == "Test Capability"
    assert descriptor.version == "1.0.0"


def test_capability_descriptor_stores_description() -> None:
    descriptor = create_capability_descriptor()

    assert (
        descriptor.description
        == "Capability used for contract auditing."
    )


def test_capability_descriptor_stores_entry_point() -> None:
    descriptor = create_capability_descriptor()

    assert (
        descriptor.entry_point
        == (
            "tests.capabilities.models."
            "test_capability_contract_audit.TestCapability"
        )
    )


def test_capability_descriptor_stores_dependencies_as_frozenset() -> None:
    descriptor = create_capability_descriptor()

    assert isinstance(
        descriptor.dependencies,
        frozenset,
    )

    assert descriptor.dependencies == frozenset(
        {
            "dependency.one",
            "dependency.two",
        }
    )


def test_capability_descriptor_is_hashable() -> None:
    descriptor = create_capability_descriptor()

    assert hash(descriptor) is not None


def test_capability_descriptor_equality_is_value_based() -> None:
    first = create_capability_descriptor()
    second = create_capability_descriptor()

    assert first == second


def test_capability_descriptor_distinguishes_different_capabilities() -> None:
    first = create_capability_descriptor()

    second = CapabilityDescriptor(
        id="different.capability",
        name=first.name,
        description=first.description,
        version=first.version,
        entry_point=first.entry_point,
        dependencies=first.dependencies,
    )

    assert first != second


def test_capability_descriptor_contract_is_minimal() -> None:
    descriptor_fields = {
        field.name
        for field in fields(CapabilityDescriptor)
    }

    expected_fields = {
        "id",
        "name",
        "description",
        "version",
        "entry_point",
        "dependencies",
        "input_contract",
        "output_contract",
    }

    assert descriptor_fields == expected_fields