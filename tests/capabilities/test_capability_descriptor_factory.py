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