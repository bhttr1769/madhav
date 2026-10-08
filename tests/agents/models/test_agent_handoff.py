import pytest

from brain.agents.models.agent_handoff import AgentHandoff


def create_handoff() -> AgentHandoff:
    return AgentHandoff(
        task_id="task-1",
        from_agent_id="agent-1",
        to_agent_id="agent-2",
        message_id="message-1",
    )


def test_creates_valid_handoff() -> None:
    handoff = create_handoff()

    assert handoff.task_id == "task-1"
    assert handoff.from_agent_id == "agent-1"
    assert handoff.to_agent_id == "agent-2"
    assert handoff.message_id == "message-1"


@pytest.mark.parametrize(
    "task_id",
    ["", "   ", None, 123],
)
def test_rejects_invalid_task_id(
    task_id: object,
) -> None:
    with pytest.raises((TypeError, ValueError)):
        AgentHandoff(
            task_id=task_id,
            from_agent_id="agent-1",
            to_agent_id="agent-2",
            message_id="message-1",
        )


@pytest.mark.parametrize(
    "from_agent_id",
    ["", "   ", None, 123],
)
def test_rejects_invalid_from_agent_id(
    from_agent_id: object,
) -> None:
    with pytest.raises((TypeError, ValueError)):
        AgentHandoff(
            task_id="task-1",
            from_agent_id=from_agent_id,
            to_agent_id="agent-2",
            message_id="message-1",
        )


@pytest.mark.parametrize(
    "to_agent_id",
    ["", "   ", None, 123],
)
def test_rejects_invalid_to_agent_id(
    to_agent_id: object,
) -> None:
    with pytest.raises((TypeError, ValueError)):
        AgentHandoff(
            task_id="task-1",
            from_agent_id="agent-1",
            to_agent_id=to_agent_id,
            message_id="message-1",
        )


def test_rejects_self_handoff() -> None:
    with pytest.raises(
        ValueError,
        match="must be different",
    ):
        AgentHandoff(
            task_id="task-1",
            from_agent_id="agent-1",
            to_agent_id="agent-1",
            message_id="message-1",
        )


@pytest.mark.parametrize(
    "message_id",
    ["", "   ", None, 123],
)
def test_rejects_invalid_message_id(
    message_id: object,
) -> None:
    with pytest.raises((TypeError, ValueError)):
        AgentHandoff(
            task_id="task-1",
            from_agent_id="agent-1",
            to_agent_id="agent-2",
            message_id=message_id,
        )


def test_handoff_is_immutable() -> None:
    handoff = create_handoff()

    with pytest.raises(AttributeError):
        handoff.task_id = "task-2"