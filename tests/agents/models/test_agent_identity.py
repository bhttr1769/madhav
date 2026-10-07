from dataclasses import FrozenInstanceError

import pytest

from brain.agents.models.agent_identity import AgentIdentity


def test_agent_identity_stores_id_and_name():
    identity = AgentIdentity(
        id="agent-001",
        name="Research Agent",
    )

    assert identity.id == "agent-001"
    assert identity.name == "Research Agent"


def test_agent_identity_is_immutable():
    identity = AgentIdentity(
        id="agent-001",
        name="Research Agent",
    )

    with pytest.raises(FrozenInstanceError):
        identity.name = "Changed"


def test_agent_identity_equality():
    first = AgentIdentity(
        id="agent-001",
        name="Research Agent",
    )

    second = AgentIdentity(
        id="agent-001",
        name="Research Agent",
    )

    assert first == second