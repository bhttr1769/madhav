from brain.agents.persistence.agent_communication_persistence import (
    AgentCommunicationPersistence,
)


def test_agent_communication_persistence_is_abstract() -> None:
    assert AgentCommunicationPersistence.__abstractmethods__ == {
        "save",
        "load",
    }