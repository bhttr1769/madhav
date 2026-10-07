from brain.agents.agent_definition_validator import (
    AgentDefinitionValidator,
)
from brain.agents.agent_registry import AgentRegistry
from brain.agents.models.agent_definition import (
    AgentDefinition,
)
from brain.agents.models.agent_identity import (
    AgentIdentity,
)


def create_agent():
    return AgentDefinition(
        identity=AgentIdentity(
            id="agent-001",
            name="Research Agent",
        ),
        description="Research agent.",
        version="1.0.0",
        capabilities=frozenset(
            {
                "knowledge.search",
                "document.read",
            }
        ),
    )


def test_valid_agent_definition_can_be_validated_and_registered():
    agent = create_agent()

    AgentDefinitionValidator().validate(agent)

    registry = AgentRegistry()
    registry.register(agent)

    assert registry.get("agent-001") is agent


def test_registry_preserves_agent_definition_without_duplication():
    agent = create_agent()

    registry = AgentRegistry()
    registry.register(agent)

    registered = registry.get("agent-001")

    assert registered is agent
    assert registered.identity is agent.identity
    assert registered.capabilities == agent.capabilities


def test_agent_capability_references_remain_ids():
    agent = create_agent()

    assert agent.capabilities == frozenset(
        {
            "knowledge.search",
            "document.read",
        }
    )