from brain.agents.communication.agent_communicator import (
    AgentCommunicator,
)


def test_agent_communicator_is_abstract() -> None:
    assert AgentCommunicator.__abstractmethods__ == {
        "send",
    }