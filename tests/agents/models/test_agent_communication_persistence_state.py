import pytest

from brain.agents.models.agent_communication_persistence_state import (
    AgentCommunicationPersistenceState,
)
from brain.agents.models.agent_handoff import AgentHandoff
from brain.agents.models.agent_message import (
    AgentMessage,
    AgentMessageType,
)


def create_message() -> AgentMessage:
    return AgentMessage(
        id="message-1",
        sender_agent_id="agent-1",
        recipient_agent_id="agent-2",
        message_type=AgentMessageType.INFORMATION,
        payload={
            "content": "Implementation completed",
        },
    )


def create_handoff() -> AgentHandoff:
    return AgentHandoff(
        task_id="task-1",
        from_agent_id="agent-1",
        to_agent_id="agent-2",
        message_id="message-1",
    )


def test_creates_valid_persistence_state() -> None:
    state = AgentCommunicationPersistenceState(
        messages=(create_message(),),
        handoffs=(create_handoff(),),
    )

    assert state.messages == (create_message(),)
    assert state.handoffs == (create_handoff(),)


def test_allows_empty_state() -> None:
    state = AgentCommunicationPersistenceState(
        messages=(),
        handoffs=(),
    )

    assert state.messages == ()
    assert state.handoffs == ()


def test_rejects_non_tuple_messages() -> None:
    with pytest.raises(TypeError, match="messages"):
        AgentCommunicationPersistenceState(
            messages=[],
            handoffs=(),
        )


def test_rejects_invalid_message_entries() -> None:
    with pytest.raises(
        TypeError,
        match="AgentMessage",
    ):
        AgentCommunicationPersistenceState(
            messages=("invalid",),
            handoffs=(),
        )


def test_rejects_non_tuple_handoffs() -> None:
    with pytest.raises(TypeError, match="handoffs"):
        AgentCommunicationPersistenceState(
            messages=(),
            handoffs=[],
        )


def test_rejects_invalid_handoff_entries() -> None:
    with pytest.raises(
        TypeError,
        match="AgentHandoff",
    ):
        AgentCommunicationPersistenceState(
            messages=(),
            handoffs=("invalid",),
        )


def test_persistence_state_is_immutable() -> None:
    state = AgentCommunicationPersistenceState(
        messages=(create_message(),),
        handoffs=(create_handoff(),),
    )

    with pytest.raises(AttributeError):
        state.messages = ()