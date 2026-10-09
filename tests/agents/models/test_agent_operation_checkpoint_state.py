import pytest

from brain.agents.models.agent_operation import (
    AgentOperation,
    AgentOperationStatus,
)
from brain.agents.models.agent_operation_checkpoint_state import (
    AgentOperationCheckpointState,
)


@pytest.fixture
def operation() -> AgentOperation:
    return AgentOperation(
        id="operation-1",
        goal_id="goal-1",
        workflow_id="workflow-1",
        status=AgentOperationStatus.PAUSED,
    )


def test_checkpoint_state_accepts_operation(
    operation: AgentOperation,
) -> None:
    state = AgentOperationCheckpointState(operation=operation)

    assert state.operation is operation


def test_checkpoint_state_rejects_invalid_operation() -> None:
    with pytest.raises(
        TypeError,
        match="operation must be an AgentOperation",
    ):
        AgentOperationCheckpointState(operation="invalid")


def test_checkpoint_state_is_immutable(
    operation: AgentOperation,
) -> None:
    state = AgentOperationCheckpointState(operation=operation)

    with pytest.raises(AttributeError):
        state.operation = AgentOperation(
            id="operation-2",
            goal_id="goal-1",
            workflow_id="workflow-1",
        )


def test_checkpoint_state_preserves_paused_operation(
    operation: AgentOperation,
) -> None:
    state = AgentOperationCheckpointState(operation=operation)

    assert state.operation.id == "operation-1"
    assert state.operation.goal_id == "goal-1"
    assert state.operation.workflow_id == "workflow-1"
    assert state.operation.status is AgentOperationStatus.PAUSED