from brain.agents.models.agent_definition import AgentDefinition
from brain.agents.models.agent_identity import AgentIdentity
from brain.capabilities.capability_registry import CapabilityRegistry
from brain.capabilities.models.capability_descriptor import (
    CapabilityDescriptor,
)


def test_agent_definition_capabilities_resolve_from_registry():
    research_capability = CapabilityDescriptor(
        id="research.execute",
        name="Research",
        description="Performs research.",
        version="1.0.0",
        entry_point="brain.research.ResearchCapability",
        dependencies=frozenset(),
    )

    browser_capability = CapabilityDescriptor(
        id="browser.navigate",
        name="Browser Navigation",
        description="Navigates a browser.",
        version="1.0.0",
        entry_point="brain.browser.BrowserCapability",
        dependencies=frozenset(),
    )

    registry = CapabilityRegistry(
        capabilities=(
            research_capability,
            browser_capability,
        )
    )

    definition = AgentDefinition(
        identity=AgentIdentity(
            id="research-agent",
            name="Research Agent",
        ),
        description="Agent for research tasks.",
        version="1.0.0",
        capabilities=frozenset(
            {
                "research.execute",
                "browser.navigate",
            }
        ),
    )

    resolved = tuple(
        registry.get(capability_id)
        for capability_id in definition.capabilities
    )

    assert set(
        capability.id
        for capability in resolved
    ) == {
        "research.execute",
        "browser.navigate",
    }


def test_agent_definition_does_not_duplicate_capability_descriptors():
    capability = CapabilityDescriptor(
        id="research.execute",
        name="Research",
        description="Performs research.",
        version="1.0.0",
        entry_point="brain.research.ResearchCapability",
        dependencies=frozenset(),
    )

    registry = CapabilityRegistry(
        capabilities=(capability,)
    )

    definition = AgentDefinition(
        identity=AgentIdentity(
            id="research-agent",
            name="Research Agent",
        ),
        description="Agent for research tasks.",
        version="1.0.0",
        capabilities=frozenset(
            {"research.execute"}
        ),
    )

    assert definition.capabilities == frozenset(
        {"research.execute"}
    )

    assert registry.get(
        "research.execute"
    ) is capability