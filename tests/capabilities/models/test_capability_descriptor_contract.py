from dataclasses import fields

from brain.capabilities.models.capability_descriptor import (
    CapabilityDescriptor,
)


def create_capability_descriptor() -> CapabilityDescriptor:
    return CapabilityDescriptor(
        id="test.capability",
        name="Test Capability",
        description="Capability used for contract testing.",
        version="1.0.0",
        entry_point=(
            "tests.capabilities.models."
            "test_capability_descriptor_contract.TestCapability"
        ),
        dependencies=frozenset(),
        input_contract="text",
        output_contract="text",
    )


class TestCapability:
    def execute(
        self,
        input_data: object,
    ) -> object:
        return input_data


def test_capability_descriptor_has_input_contract() -> None:
    descriptor = create_capability_descriptor()

    assert descriptor.input_contract == "text"


def test_capability_descriptor_has_output_contract() -> None:
    descriptor = create_capability_descriptor()

    assert descriptor.output_contract == "text"


def test_capability_descriptor_contracts_are_strings() -> None:
    descriptor = create_capability_descriptor()

    assert isinstance(
        descriptor.input_contract,
        str,
    )

    assert isinstance(
        descriptor.output_contract,
        str,
    )


def test_capability_descriptor_contracts_are_part_of_the_dataclass() -> None:
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


def test_capability_descriptor_defaults_to_generic_contracts() -> None:
    descriptor = CapabilityDescriptor(
        id="test.capability",
        name="Test Capability",
        description="Capability using default contracts.",
        version="1.0.0",
        entry_point="tests.capabilities.TestCapability",
        dependencies=frozenset(),
    )

    assert descriptor.input_contract == "object"
    assert descriptor.output_contract == "object"


def test_capability_descriptor_remains_immutable() -> None:
    descriptor = create_capability_descriptor()

    try:
        descriptor.input_contract = "number"
    except AttributeError:
        pass
    else:
        raise AssertionError(
            "CapabilityDescriptor must remain immutable."
        )


def test_capability_descriptor_contracts_participate_in_equality() -> None:
    first = create_capability_descriptor()

    second = CapabilityDescriptor(
        id=first.id,
        name=first.name,
        description=first.description,
        version=first.version,
        entry_point=first.entry_point,
        dependencies=first.dependencies,
        input_contract="different",
        output_contract=first.output_contract,
    )

    assert first != second