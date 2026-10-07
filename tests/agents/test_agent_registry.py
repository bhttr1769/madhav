import pytest

from brain.agents.agent_registry import AgentRegistry
from brain.agents.models.agent_definition import (
    AgentDefinition,
)
from brain.agents.models.agent_identity import (
    AgentIdentity,
)


def create_agent(
    agent_id="agent-001",
    name="Research Agent",
):
    return AgentDefinition(
        identity=AgentIdentity(
            id=agent_id,
            name=name,
        ),
        description="Research agent.",
        version="1.0.0",
        capabilities=frozenset(),
    )


def test_registry_starts_empty():
    registry = AgentRegistry()

    assert registry.all() == ()


def test_register_and_get_agent():
    registry = AgentRegistry()
    agent = create_agent()

    registry.register(agent)

    assert registry.get("agent-001") == agent


def test_register_duplicate_agent_raises_value_error():
    registry = AgentRegistry()
    agent = create_agent()

    registry.register(agent)

    with pytest.raises(ValueError):
        registry.register(agent)


def test_get_missing_agent_raises_key_error():
    registry = AgentRegistry()

    with pytest.raises(KeyError):
        registry.get("missing-agent")


def test_has_returns_true_for_registered_agent():
    registry = AgentRegistry()
    agent = create_agent()

    registry.register(agent)

    assert registry.has("agent-001") is True


def test_has_returns_false_for_missing_agent():
    registry = AgentRegistry()

    assert registry.has("missing-agent") is False


def test_all_returns_registered_agents():
    first = create_agent(
        agent_id="agent-001",
        name="Research Agent",
    )
    second = create_agent(
        agent_id="agent-002",
        name="Coding Agent",
    )

    registry = AgentRegistry(
        agents=(first, second)
    )

    assert registry.all() == (
        first,
        second,
    )


def test_unregister_removes_agent():
    registry = AgentRegistry()
    agent = create_agent()

    registry.register(agent)
    registry.unregister("agent-001")

    assert registry.has("agent-001") is False
    assert registry.all() == ()


def test_unregister_missing_agent_raises_key_error():
    registry = AgentRegistry()

    with pytest.raises(KeyError):
        registry.unregister("missing-agent")


def test_register_invalid_type_raises_type_error():
    registry = AgentRegistry()

    with pytest.raises(TypeError):
        registry.register(object())