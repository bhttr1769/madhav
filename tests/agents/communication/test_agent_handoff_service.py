from brain.agents.communication.agent_handoff_service import (
    AgentHandoffService,
)


def test_agent_handoff_service_is_abstract() -> None:
    assert AgentHandoffService.__abstractmethods__ == {
        "handoff",
    }