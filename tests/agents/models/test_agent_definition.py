from dataclasses import FrozenInstanceError

import pytest

from brain.agents.models.agent_definition import AgentDefinition
from brain.agents.models.agent_identity import AgentIdentity


def test_agent_definition_stores_identity_and_metadata():
    identity = AgentIdentity(
        id="agent-001",
        name="Research Agent",
    )

    definition = AgentDefinition(
        identity=identity,
        description="Agent responsible for research tasks.",
        version="1.0.0",
        capabilities=frozenset(
            {
                "document.read",
                "browser.navigate",
            }
        ),
    )

    assert definition.identity == identity
    assert definition.description == "Agent responsible for research tasks."
    assert definition.version == "1.0.0"
    assert definition.capabilities == frozenset(
        {
            "document.read",
            "browser.navigate",
        }
    )


def test_agent_definition_allows_empty_capabilities():
    identity = AgentIdentity(
        id="agent-001",
        name="Research Agent",
    )

    definition = AgentDefinition(
        identity=identity,
        description="Agent without assigned capabilities.",
        version="1.0.0",
        capabilities=frozenset(),
    )

    assert definition.capabilities == frozenset()


def test_agent_definition_is_immutable():
    identity = AgentIdentity(
        id="agent-001",
        name="Research Agent",
    )

    definition = AgentDefinition(
        identity=identity,
        description="Research agent.",
        version="1.0.0",
        capabilities=frozenset(),
    )

    with pytest.raises(FrozenInstanceError):
        definition.version = "2.0.0"


def test_agent_definition_equality():
    identity = AgentIdentity(
        id="agent-001",
        name="Research Agent",
    )

    first = AgentDefinition(
        identity=identity,
        description="Research agent.",
        version="1.0.0",
        capabilities=frozenset({"document.read"}),
    )

    second = AgentDefinition(
        identity=identity,
        description="Research agent.",
        version="1.0.0",
        capabilities=frozenset({"document.read"}),
    )

    assert first == second