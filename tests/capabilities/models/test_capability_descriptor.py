from dataclasses import FrozenInstanceError

import pytest

from brain.capabilities.models.capability_descriptor import (
    CapabilityDescriptor,
)


def test_capability_descriptor_stores_metadata():
    capability = CapabilityDescriptor(
        id="web_research",
        name="Web Research",
        description="Research external information.",
        version="1.0.0",
        entry_point="brain.research.ResearchEngine",
        dependencies=frozenset(
            {"web_search"}
        ),
    )

    assert capability.id == "web_research"
    assert capability.name == "Web Research"
    assert capability.description == (
        "Research external information."
    )
    assert capability.version == "1.0.0"
    assert capability.entry_point == (
        "brain.research.ResearchEngine"
    )
    assert capability.dependencies == frozenset(
        {"web_search"}
    )


def test_capability_descriptor_is_immutable():
    capability = CapabilityDescriptor(
        id="test",
        name="Test",
        description="Test capability.",
        version="1.0.0",
        entry_point="brain.test.Test",
        dependencies=frozenset(),
    )

    with pytest.raises(FrozenInstanceError):
        capability.name = "Changed"


def test_capability_descriptor_dependencies_are_immutable():
    capability = CapabilityDescriptor(
        id="test",
        name="Test",
        description="Test capability.",
        version="1.0.0",
        entry_point="brain.test.Test",
        dependencies=frozenset({"base"}),
    )

    assert isinstance(
        capability.dependencies,
        frozenset,
    )