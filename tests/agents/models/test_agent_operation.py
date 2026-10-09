from dataclasses import FrozenInstanceError

import pytest

from brain.agents.models.agent_operation import (
    AgentOperation,
    AgentOperationStatus,
)


def create_operation() -> AgentOperation:
    return AgentOperation(
        id="operation-1",
        goal_id="goal-1",
        workflow_id="workflow-1",
    )


def test_creates_operation_with_default_status() -> None:
    operation = create_operation()

    assert operation.status is AgentOperationStatus.CREATED


@pytest.mark.parametrize(
    "field_name",
    ("id", "goal_id", "workflow_id"),
)
def test_rejects_empty_identifiers(field_name: str) -> None:
    values = {
        "id": "operation-1",
        "goal_id": "goal-1",
        "workflow_id": "workflow-1",
    }
    values[field_name] = "   "

    with pytest.raises(ValueError, match=field_name):
        AgentOperation(**values)


@pytest.mark.parametrize(
    "field_name",
    ("id", "goal_id", "workflow_id"),
)
def test_rejects_non_string_identifiers(field_name: str) -> None:
    values = {
        "id": "operation-1",
        "goal_id": "goal-1",
        "workflow_id": "workflow-1",
    }
    values[field_name] = 123

    with pytest.raises(TypeError, match=field_name):
        AgentOperation(**values)


def test_rejects_invalid_status() -> None:
    with pytest.raises(TypeError, match="AgentOperationStatus"):
        AgentOperation(
            id="operation-1",
            goal_id="goal-1",
            workflow_id="workflow-1",
            status="running",
        )


def test_operation_is_immutable() -> None:
    operation = create_operation()

    with pytest.raises(FrozenInstanceError):
        operation.status = AgentOperationStatus.RUNNING