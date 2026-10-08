import pytest

from brain.agents.agent_registry import AgentRegistry
from brain.agents.communication.agent_message_router import (
    AgentMessageRouter,
)
from brain.agents.models.agent_definition import AgentDefinition
from brain.agents.models.agent_identity import AgentIdentity
from brain.agents.models.agent_message import (
    AgentMessage,
    AgentMessageType,
)


def create_registry() -> AgentRegistry:
    registry = AgentRegistry()

    registry.register(
        AgentDefinition(
            identity=AgentIdentity(
                id="agent-1",
                name="Agent One",
            ),
            description="First agent",
            version="1.0",
            capabilities=frozenset(),
        )
    )

    registry.register(
        AgentDefinition(
            identity=AgentIdentity(
                id="agent-2",
                name="Agent Two",
            ),
            description="Second agent",
            version="1.0",
            capabilities=frozenset(),
        )
    )

    return registry


def create_message(
    message_id: str = "message-1",
    recipient_agent_id: str = "agent-2",
    message_type: AgentMessageType = AgentMessageType.INFORMATION,
    correlation_id: str | None = None,
) -> AgentMessage:
    return AgentMessage(
        id=message_id,
        sender_agent_id="agent-1",
        recipient_agent_id=recipient_agent_id,
        message_type=message_type,
        payload={
            "content": "Implementation completed",
        },
        correlation_id=correlation_id,
    )


def test_delivers_message_to_registered_recipient() -> None:
    router = AgentMessageRouter(create_registry())

    message = create_message()

    router.send(message)

    assert router.messages_for("agent-2") == (message,)


def test_delivers_multiple_messages_in_order() -> None:
    router = AgentMessageRouter(create_registry())

    message_1 = create_message()

    message_2 = create_message(
        message_id="message-2",
        message_type=AgentMessageType.RESPONSE,
    )

    router.send(message_1)
    router.send(message_2)

    assert router.messages_for("agent-2") == (
        message_1,
        message_2,
    )


def test_does_not_mix_messages_between_recipients() -> None:
    router = AgentMessageRouter(create_registry())

    message = create_message("message-1", "agent-2")

    router.send(message)

    assert router.messages_for("agent-1") == ()
    assert router.messages_for("agent-2") == (message,)


def test_rejects_unknown_recipient() -> None:
    router = AgentMessageRouter(create_registry())

    message = create_message(
        recipient_agent_id="unknown-agent",
    )

    with pytest.raises(
        ValueError,
        match="Recipient agent is not registered",
    ):
        router.send(message)


def test_rejects_invalid_message() -> None:
    router = AgentMessageRouter(create_registry())

    with pytest.raises(
        TypeError,
        match="message",
    ):
        router.send("invalid")


def test_messages_for_returns_tuple() -> None:
    router = AgentMessageRouter(create_registry())

    message = create_message()

    router.send(message)

    messages = router.messages_for("agent-2")

    assert isinstance(messages, tuple)
    assert messages == (message,)


def test_rejects_invalid_agent_id() -> None:
    router = AgentMessageRouter(create_registry())

    with pytest.raises(
        TypeError,
        match="agent_id",
    ):
        router.messages_for(123)


def test_rejects_empty_agent_id() -> None:
    router = AgentMessageRouter(create_registry())

    with pytest.raises(
        ValueError,
        match="agent_id",
    ):
        router.messages_for("   ")


def test_request_can_have_no_correlation_id() -> None:
    message = create_message(
        message_type=AgentMessageType.REQUEST,
    )

    assert message.correlation_id is None


def test_response_can_reference_request() -> None:
    request = create_message(
        message_id="request-1",
        message_type=AgentMessageType.REQUEST,
    )

    response = create_message(
        message_id="response-1",
        message_type=AgentMessageType.RESPONSE,
        correlation_id=request.id,
    )

    assert response.correlation_id == "request-1"


def test_messages_for_correlation_returns_matching_messages() -> None:
    router = AgentMessageRouter(create_registry())

    request = create_message(
        message_id="request-1",
        message_type=AgentMessageType.REQUEST,
    )

    response = create_message(
        message_id="response-1",
        message_type=AgentMessageType.RESPONSE,
        correlation_id="request-1",
    )

    router.send(request)
    router.send(response)

    assert router.messages_for_correlation(
        "agent-2",
        "request-1",
    ) == (response,)


def test_messages_for_correlation_excludes_unrelated_messages() -> None:
    router = AgentMessageRouter(create_registry())

    response_1 = create_message(
        message_id="response-1",
        message_type=AgentMessageType.RESPONSE,
        correlation_id="request-1",
    )

    response_2 = create_message(
        message_id="response-2",
        message_type=AgentMessageType.RESPONSE,
        correlation_id="request-2",
    )

    router.send(response_1)
    router.send(response_2)

    assert router.messages_for_correlation(
        "agent-2",
        "request-1",
    ) == (response_1,)


def test_messages_for_correlation_preserves_order() -> None:
    router = AgentMessageRouter(create_registry())

    response_1 = create_message(
        message_id="response-1",
        message_type=AgentMessageType.RESPONSE,
        correlation_id="request-1",
    )

    response_2 = create_message(
        message_id="response-2",
        message_type=AgentMessageType.RESPONSE,
        correlation_id="request-1",
    )

    router.send(response_1)
    router.send(response_2)

    assert router.messages_for_correlation(
        "agent-2",
        "request-1",
    ) == (
        response_1,
        response_2,
    )


def test_messages_for_correlation_does_not_mix_recipients() -> None:
    router = AgentMessageRouter(create_registry())

    message = create_message(
        message_id="response-1",
        recipient_agent_id="agent-2",
        message_type=AgentMessageType.RESPONSE,
        correlation_id="request-1",
    )

    router.send(message)

    assert router.messages_for_correlation(
        "agent-1",
        "request-1",
    ) == ()

    assert router.messages_for_correlation(
        "agent-2",
        "request-1",
    ) == (message,)


def test_rejects_invalid_correlation_id() -> None:
    router = AgentMessageRouter(create_registry())

    with pytest.raises(
        TypeError,
        match="correlation_id",
    ):
        router.messages_for_correlation(
            "agent-2",
            123,
        )


def test_rejects_empty_correlation_id() -> None:
    router = AgentMessageRouter(create_registry())

    with pytest.raises(
        ValueError,
        match="correlation_id",
    ):
        router.messages_for_correlation(
            "agent-2",
            "   ",
        )