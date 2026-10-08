import pytest

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


def test_creates_valid_message() -> None:
    message = create_message()

    assert message.id == "message-1"
    assert message.sender_agent_id == "agent-1"
    assert message.recipient_agent_id == "agent-2"
    assert message.message_type is AgentMessageType.INFORMATION
    assert message.payload == {
        "content": "Implementation completed",
    }


def test_supports_all_message_types() -> None:
    assert set(AgentMessageType) == {
        AgentMessageType.INFORMATION,
        AgentMessageType.REQUEST,
        AgentMessageType.RESPONSE,
        AgentMessageType.HANDOFF,
    }


@pytest.mark.parametrize(
    "message_id",
    [
        "",
        "   ",
        None,
        123,
    ],
)
def test_rejects_invalid_message_id(message_id: object) -> None:
    with pytest.raises((TypeError, ValueError)):
        AgentMessage(
            id=message_id,
            sender_agent_id="agent-1",
            recipient_agent_id="agent-2",
            message_type=AgentMessageType.INFORMATION,
            payload={},
        )


@pytest.mark.parametrize(
    "sender_agent_id",
    [
        "",
        "   ",
        None,
        123,
    ],
)
def test_rejects_invalid_sender_agent_id(
    sender_agent_id: object,
) -> None:
    with pytest.raises((TypeError, ValueError)):
        AgentMessage(
            id="message-1",
            sender_agent_id=sender_agent_id,
            recipient_agent_id="agent-2",
            message_type=AgentMessageType.INFORMATION,
            payload={},
        )


@pytest.mark.parametrize(
    "recipient_agent_id",
    [
        "",
        "   ",
        None,
        123,
    ],
)
def test_rejects_invalid_recipient_agent_id(
    recipient_agent_id: object,
) -> None:
    with pytest.raises((TypeError, ValueError)):
        AgentMessage(
            id="message-1",
            sender_agent_id="agent-1",
            recipient_agent_id=recipient_agent_id,
            message_type=AgentMessageType.INFORMATION,
            payload={},
        )


def test_rejects_invalid_message_type() -> None:
    with pytest.raises(TypeError, match="message_type"):
        AgentMessage(
            id="message-1",
            sender_agent_id="agent-1",
            recipient_agent_id="agent-2",
            message_type="information",
            payload={},
        )


@pytest.mark.parametrize(
    "payload",
    [
        [],
        (),
        "payload",
        None,
    ],
)
def test_rejects_non_dict_payload(
    payload: object,
) -> None:
    with pytest.raises(TypeError, match="payload"):
        AgentMessage(
            id="message-1",
            sender_agent_id="agent-1",
            recipient_agent_id="agent-2",
            message_type=AgentMessageType.INFORMATION,
            payload=payload,
        )


def test_message_is_immutable() -> None:
    message = create_message()

    with pytest.raises(AttributeError):
        message.id = "message-2"