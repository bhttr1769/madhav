import pytest

from brain.capabilities.capability_descriptor_factory import (
    CapabilityDescriptorFactory,
)
from brain.capabilities.models.capability_descriptor import (
    CapabilityDescriptor,
)
from brain.capabilities.models.capability_descriptor_request import (
    CapabilityDescriptorRequest,
)


def _request():
    return CapabilityDescriptorRequest(
        id="web_research",
        name="Web Research",
        description="Research information from the web.",
        version="1.0.0",
        entry_point="brain.research:WebResearch",
        dependencies=frozenset(),
    )


def test_factory_creates_capability_descriptor():
    factory = CapabilityDescriptorFactory()

    result = factory.create(
        _request()
    )

    assert isinstance(
        result,
        CapabilityDescriptor,
    )

    assert result.id == "web_research"
    assert result.name == "Web Research"
    assert result.description == (
        "Research information from the web."
    )
    assert result.version == "1.0.0"
    assert result.entry_point == (
        "brain.research:WebResearch"
    )
    assert result.dependencies == frozenset()


def test_factory_preserves_dependencies():
    factory = CapabilityDescriptorFactory()

    request = CapabilityDescriptorRequest(
        id="web_research",
        name="Web Research",
        description="Research information from the web.",
        version="1.0.0",
        entry_point="brain.research:WebResearch",
        dependencies=frozenset(
            {
                "requests",
                "beautifulsoup4",
            }
        ),
    )

    result = factory.create(request)

    assert result.dependencies == frozenset(
        {
            "requests",
            "beautifulsoup4",
        }
    )


def test_factory_rejects_invalid_request():
    factory = CapabilityDescriptorFactory()

    with pytest.raises(
        TypeError,
        match="request must be a CapabilityDescriptorRequest",
    ):
        factory.create(
            "web_research"
        )

def test_factory_preserves_input_contract() -> None:
    request = CapabilityDescriptorRequest(
        id="test.capability",
        name="Test Capability",
        description="Test capability.",
        version="1.0.0",
        entry_point="tests.capabilities.TestCapability",
        dependencies=frozenset(),
        input_contract="text",
        output_contract="text",
    )

    descriptor = CapabilityDescriptorFactory().create(
        request
    )

    assert descriptor.input_contract == "text"


def test_factory_preserves_output_contract() -> None:
    request = CapabilityDescriptorRequest(
        id="test.capability",
        name="Test Capability",
        description="Test capability.",
        version="1.0.0",
        entry_point="tests.capabilities.TestCapability",
        dependencies=frozenset(),
        input_contract="text",
        output_contract="number",
    )

    descriptor = CapabilityDescriptorFactory().create(
        request
    )

    assert descriptor.output_contract == "number"


def test_factory_preserves_default_contracts() -> None:
    request = CapabilityDescriptorRequest(
        id="test.capability",
        name="Test Capability",
        description="Test capability.",
        version="1.0.0",
        entry_point="tests.capabilities.TestCapability",
        dependencies=frozenset(),
    )

    descriptor = CapabilityDescriptorFactory().create(
        request
    )

    assert descriptor.input_contract == "object"
    assert descriptor.output_contract == "object"


def test_factory_preserves_all_descriptor_fields() -> None:
    request = CapabilityDescriptorRequest(
        id="test.capability",
        name="Test Capability",
        description="Test capability.",
        version="1.0.0",
        entry_point="tests.capabilities.TestCapability",
        dependencies=frozenset(
            {
                "dependency.one",
                "dependency.two",
            }
        ),
        input_contract="text",
        output_contract="number",
    )

    descriptor = CapabilityDescriptorFactory().create(
        request
    )

    assert descriptor.id == request.id
    assert descriptor.name == request.name
    assert descriptor.description == request.description
    assert descriptor.version == request.version
    assert descriptor.entry_point == request.entry_point
    assert descriptor.dependencies == request.dependencies
    assert descriptor.input_contract == request.input_contract
    assert descriptor.output_contract == request.output_contract