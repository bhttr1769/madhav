import pytest

from brain.agents.agent_operation_lifecycle import AgentOperationLifecycle
from brain.agents.models.agent_operation import (
    AgentOperation,
    AgentOperationStatus,
)


@pytest.fixture
def lifecycle() -> AgentOperationLifecycle:
    return AgentOperationLifecycle()


@pytest.fixture
def operation() -> AgentOperation:
    return AgentOperation(
        id="operation-1",
        goal_id="goal-1",
        workflow_id="workflow-1",
    )


@pytest.mark.parametrize(
    ("current_status", "target_status"),
    [
        (
            AgentOperationStatus.CREATED,
            AgentOperationStatus.RUNNING,
        ),
        (
            AgentOperationStatus.CREATED,
            AgentOperationStatus.CANCELLED,
        ),
        (
            AgentOperationStatus.RUNNING,
            AgentOperationStatus.PAUSED,
        ),
        (
            AgentOperationStatus.RUNNING,
            AgentOperationStatus.COMPLETED,
        ),
        (
            AgentOperationStatus.RUNNING,
            AgentOperationStatus.FAILED,
        ),
        (
            AgentOperationStatus.RUNNING,
            AgentOperationStatus.CANCELLED,
        ),
        (
            AgentOperationStatus.PAUSED,
            AgentOperationStatus.RUNNING,
        ),
        (
            AgentOperationStatus.PAUSED,
            AgentOperationStatus.FAILED,
        ),
        (
            AgentOperationStatus.PAUSED,
            AgentOperationStatus.CANCELLED,
        ),
    ],
)
def test_can_transition_returns_true_for_allowed_transitions(
    lifecycle: AgentOperationLifecycle,
    current_status: AgentOperationStatus,
    target_status: AgentOperationStatus,
) -> None:
    assert lifecycle.can_transition(current_status, target_status)


@pytest.mark.parametrize(
    ("current_status", "target_status"),
    [
        (
            AgentOperationStatus.CREATED,
            AgentOperationStatus.PAUSED,
        ),
        (
            AgentOperationStatus.CREATED,
            AgentOperationStatus.COMPLETED,
        ),
        (
            AgentOperationStatus.CREATED,
            AgentOperationStatus.FAILED,
        ),
        (
            AgentOperationStatus.RUNNING,
            AgentOperationStatus.CREATED,
        ),
        (
            AgentOperationStatus.PAUSED,
            AgentOperationStatus.CREATED,
        ),
        (
            AgentOperationStatus.COMPLETED,
            AgentOperationStatus.RUNNING,
        ),
        (
            AgentOperationStatus.FAILED,
            AgentOperationStatus.RUNNING,
        ),
        (
            AgentOperationStatus.CANCELLED,
            AgentOperationStatus.RUNNING,
        ),
    ],
)
def test_can_transition_returns_false_for_disallowed_transitions(
    lifecycle: AgentOperationLifecycle,
    current_status: AgentOperationStatus,
    target_status: AgentOperationStatus,
) -> None:
    assert not lifecycle.can_transition(current_status, target_status)


@pytest.mark.parametrize(
    "terminal_status",
    [
        AgentOperationStatus.COMPLETED,
        AgentOperationStatus.FAILED,
        AgentOperationStatus.CANCELLED,
    ],
)
def test_terminal_states_cannot_transition(
    lifecycle: AgentOperationLifecycle,
    terminal_status: AgentOperationStatus,
) -> None:
    for target_status in AgentOperationStatus:
        assert not lifecycle.can_transition(terminal_status, target_status)


def test_transition_returns_new_operation(
    lifecycle: AgentOperationLifecycle,
    operation: AgentOperation,
) -> None:
    updated = lifecycle.transition(
        operation,
        AgentOperationStatus.RUNNING,
    )

    assert updated is not operation
    assert updated.id == operation.id
    assert updated.goal_id == operation.goal_id
    assert updated.workflow_id == operation.workflow_id
    assert updated.status is AgentOperationStatus.RUNNING


def test_transition_does_not_mutate_original_operation(
    lifecycle: AgentOperationLifecycle,
    operation: AgentOperation,
) -> None:
    original_status = operation.status

    lifecycle.transition(operation, AgentOperationStatus.RUNNING)

    assert operation.status is original_status
    assert operation.status is AgentOperationStatus.CREATED


def test_transition_rejects_invalid_transition(
    lifecycle: AgentOperationLifecycle,
    operation: AgentOperation,
) -> None:
    with pytest.raises(ValueError, match="Invalid operation status transition"):
        lifecycle.transition(operation, AgentOperationStatus.COMPLETED)


def test_can_transition_rejects_invalid_current_status(
    lifecycle: AgentOperationLifecycle,
) -> None:
    with pytest.raises(TypeError, match="current_status"):
        lifecycle.can_transition("created", AgentOperationStatus.RUNNING)


def test_can_transition_rejects_invalid_target_status(
    lifecycle: AgentOperationLifecycle,
) -> None:
    with pytest.raises(TypeError, match="target_status"):
        lifecycle.can_transition(AgentOperationStatus.CREATED, "running")


def test_transition_rejects_invalid_operation(
    lifecycle: AgentOperationLifecycle,
) -> None:
    with pytest.raises(TypeError, match="operation"):
        lifecycle.transition("not-an-operation", AgentOperationStatus.RUNNING)


def test_transition_rejects_invalid_target_status(
    lifecycle: AgentOperationLifecycle,
    operation: AgentOperation,
) -> None:
    with pytest.raises(TypeError, match="target_status"):
        lifecycle.transition(operation, "running")