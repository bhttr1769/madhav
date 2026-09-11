import pytest

from brain.capabilities.capability_discovery import (
    CapabilityDiscovery,
)
from brain.capabilities.models.capability_descriptor import (
    CapabilityDescriptor,
)


class WebResearchProvider:
    @staticmethod
    def capability_descriptor():
        return CapabilityDescriptor(
            id="web_research",
            name="Web Research",
            description=(
                "Research information from external sources."
            ),
            version="1.0.0",
            entry_point=(
                "brain.research.ResearchEngine"
            ),
            dependencies=frozenset(),
        )


class MemoryProvider:
    @staticmethod
    def capability_descriptor():
        return CapabilityDescriptor(
            id="memory",
            name="Memory",
            description="Store and retrieve knowledge.",
            version="1.0.0",
            entry_point="brain.memory.Memory",
            dependencies=frozenset(),
        )


class NonCapabilityProvider:
    pass


class InvalidCapabilityProvider:
    @staticmethod
    def capability_descriptor():
        return "invalid"


def test_discovery_returns_empty_when_no_providers():
    discovery = CapabilityDiscovery()

    assert discovery.discover() == ()


def test_discovery_finds_capability():
    discovery = CapabilityDiscovery(
        providers=(WebResearchProvider(),),
    )

    capabilities = discovery.discover()

    assert len(capabilities) == 1
    assert capabilities[0].id == "web_research"


def test_discovery_finds_multiple_capabilities():
    discovery = CapabilityDiscovery(
        providers=(
            WebResearchProvider(),
            MemoryProvider(),
        ),
    )

    capabilities = discovery.discover()

    assert capabilities == (
        WebResearchProvider.capability_descriptor(),
        MemoryProvider.capability_descriptor(),
    )


def test_discovery_ignores_non_capability_provider():
    discovery = CapabilityDiscovery(
        providers=(NonCapabilityProvider(),),
    )

    assert discovery.discover() == ()


def test_discovery_rejects_invalid_descriptor():
    discovery = CapabilityDiscovery(
        providers=(InvalidCapabilityProvider(),),
    )

    with pytest.raises(TypeError):
        discovery.discover()


def test_discovery_rejects_non_callable_descriptor():
    class InvalidProvider:
        capability_descriptor = "not callable"

    discovery = CapabilityDiscovery(
        providers=(InvalidProvider(),),
    )

    with pytest.raises(TypeError):
        discovery.discover()