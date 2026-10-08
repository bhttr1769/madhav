import pytest

from brain.agents.models.agent_assignment import AgentAssignment


def test_creates_valid_agent_assignment() -> None:
    assignment = AgentAssignment(
        task_id="task-1",
        agent_id="agent-1",
    )

    assert assignment.task_id == "task-1"
    assert assignment.agent_id == "agent-1"


def test_rejects_empty_task_id() -> None:
    with pytest.raises(ValueError, match="task_id"):
        AgentAssignment(
            task_id="",
            agent_id="agent-1",
        )


def test_rejects_whitespace_task_id() -> None:
    with pytest.raises(ValueError, match="task_id"):
        AgentAssignment(
            task_id="   ",
            agent_id="agent-1",
        )


def test_rejects_non_string_task_id() -> None:
    with pytest.raises(TypeError, match="task_id"):
        AgentAssignment(
            task_id=123,
            agent_id="agent-1",
        )


def test_rejects_empty_agent_id() -> None:
    with pytest.raises(ValueError, match="agent_id"):
        AgentAssignment(
            task_id="task-1",
            agent_id="",
        )


def test_rejects_whitespace_agent_id() -> None:
    with pytest.raises(ValueError, match="agent_id"):
        AgentAssignment(
            task_id="task-1",
            agent_id="   ",
        )


def test_rejects_non_string_agent_id() -> None:
    with pytest.raises(TypeError, match="agent_id"):
        AgentAssignment(
            task_id="task-1",
            agent_id=123,
        )


def test_agent_assignment_is_immutable() -> None:
    assignment = AgentAssignment(
        task_id="task-1",
        agent_id="agent-1",
    )

    with pytest.raises(AttributeError):
        assignment.task_id = "task-2"