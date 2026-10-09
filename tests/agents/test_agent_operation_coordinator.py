import pytest

from brain.agents.agent_operation_coordinator import (
    AgentOperationCoordinator,
)
from brain.agents.models.agent_operation import (
    AgentOperation,
    AgentOperationStatus,
)
from brain.agents.models.goal import Goal
from brain.agents.models.goal_status import GoalStatus
from brain.agents.models.workflow import Workflow, WorkflowStatus


@pytest.fixture
def coordinator() -> AgentOperationCoordinator:
    return AgentOperationCoordinator()


@pytest.fixture
def goal() -> Goal:
    return Goal(
        id="goal-1",
        agent_id="agent-1",
        description="Complete the assigned work",
    )


@pytest.fixture
def workflow() -> Workflow:
    return Workflow(
        id="workflow-1",
        goal_id="goal-1",
        step_ids=("step-1",),
        status=WorkflowStatus.READY,
    )


@pytest.fixture
def operation() -> AgentOperation:
    return AgentOperation(
        id="operation-1",
        goal_id="goal-1",
        workflow_id="workflow-1",
    )


def test_validate_accepts_matching_references(
    coordinator: AgentOperationCoordinator,
    operation: AgentOperation,
    goal: Goal,
    workflow: Workflow,
) -> None:
    coordinator.validate(operation, goal, workflow)


@pytest.mark.parametrize(
    ("argument", "message"),
    [
        ("operation", "operation must be an AgentOperation"),
        ("goal", "goal must be a Goal"),
        ("workflow", "workflow must be a Workflow"),
    ],
)
def test_validate_rejects_invalid_argument_types(
    coordinator: AgentOperationCoordinator,
    operation: AgentOperation,
    goal: Goal,
    workflow: Workflow,
    argument: str,
    message: str,
) -> None:
    values = {
        "operation": operation,
        "goal": goal,
        "workflow": workflow,
    }
    values[argument] = object()

    with pytest.raises(TypeError, match=message):
        coordinator.validate(
            values["operation"],
            values["goal"],
            values["workflow"],
        )


def test_validate_rejects_mismatched_goal_id(
    coordinator: AgentOperationCoordinator,
    operation: AgentOperation,
    workflow: Workflow,
) -> None:
    other_goal = Goal(
        id="goal-2",
        agent_id="agent-1",
        description="Another goal",
    )

    with pytest.raises(ValueError, match="operation goal_id"):
        coordinator.validate(operation, other_goal, workflow)


def test_validate_rejects_mismatched_workflow_id(
    coordinator: AgentOperationCoordinator,
    operation: AgentOperation,
    goal: Goal,
) -> None:
    other_workflow = Workflow(
        id="workflow-2",
        goal_id="goal-1",
        step_ids=("step-1",),
        status=WorkflowStatus.READY,
    )

    with pytest.raises(ValueError, match="operation workflow_id"):
        coordinator.validate(operation, goal, other_workflow)


def test_validate_rejects_workflow_for_another_goal(
    coordinator: AgentOperationCoordinator,
    operation: AgentOperation,
    goal: Goal,
) -> None:
    other_workflow = Workflow(
        id="workflow-1",
        goal_id="goal-2",
        step_ids=("step-1",),
        status=WorkflowStatus.READY,
    )

    with pytest.raises(ValueError, match="workflow goal_id"):
        coordinator.validate(operation, goal, other_workflow)


def test_start_returns_running_operation(
    coordinator: AgentOperationCoordinator,
    operation: AgentOperation,
    goal: Goal,
    workflow: Workflow,
) -> None:
    updated = coordinator.start(operation, goal, workflow)

    assert updated.status is AgentOperationStatus.RUNNING
    assert updated is not operation
    assert operation.status is AgentOperationStatus.CREATED


@pytest.mark.parametrize(
    "workflow_status",
    [
        WorkflowStatus.CREATED,
        WorkflowStatus.COMPLETED,
        WorkflowStatus.FAILED,
    ],
)
def test_start_rejects_workflow_that_is_not_ready_or_running(
    coordinator: AgentOperationCoordinator,
    operation: AgentOperation,
    goal: Goal,
    workflow_status: WorkflowStatus,
) -> None:
    workflow = Workflow(
        id="workflow-1",
        goal_id="goal-1",
        step_ids=("step-1",),
        status=workflow_status,
    )

    with pytest.raises(ValueError, match="workflow must be READY or RUNNING"):
        coordinator.start(operation, goal, workflow)


def test_start_accepts_running_workflow(
    coordinator: AgentOperationCoordinator,
    operation: AgentOperation,
    goal: Goal,
) -> None:
    workflow = Workflow(
        id="workflow-1",
        goal_id="goal-1",
        step_ids=("step-1",),
        status=WorkflowStatus.RUNNING,
    )

    updated = coordinator.start(operation, goal, workflow)

    assert updated.status is AgentOperationStatus.RUNNING


def test_pause_returns_paused_operation(
    coordinator: AgentOperationCoordinator,
    goal: Goal,
    workflow: Workflow,
) -> None:
    operation = AgentOperation(
        id="operation-1",
        goal_id="goal-1",
        workflow_id="workflow-1",
        status=AgentOperationStatus.RUNNING,
    )

    updated = coordinator.pause(operation, goal, workflow)

    assert updated.status is AgentOperationStatus.PAUSED
    assert operation.status is AgentOperationStatus.RUNNING


def test_resume_returns_running_operation(
    coordinator: AgentOperationCoordinator,
    goal: Goal,
) -> None:
    operation = AgentOperation(
        id="operation-1",
        goal_id="goal-1",
        workflow_id="workflow-1",
        status=AgentOperationStatus.PAUSED,
    )
    workflow = Workflow(
        id="workflow-1",
        goal_id="goal-1",
        step_ids=("step-1",),
        status=WorkflowStatus.RUNNING,
    )

    updated = coordinator.resume(operation, goal, workflow)

    assert updated.status is AgentOperationStatus.RUNNING


def test_resume_rejects_non_running_workflow(
    coordinator: AgentOperationCoordinator,
    goal: Goal,
    workflow: Workflow,
) -> None:
    operation = AgentOperation(
        id="operation-1",
        goal_id="goal-1",
        workflow_id="workflow-1",
        status=AgentOperationStatus.PAUSED,
    )

    with pytest.raises(ValueError, match="workflow must be RUNNING"):
        coordinator.resume(operation, goal, workflow)


def test_complete_accepts_completed_workflow(
    coordinator: AgentOperationCoordinator,
    goal: Goal,
) -> None:
    operation = AgentOperation(
        id="operation-1",
        goal_id="goal-1",
        workflow_id="workflow-1",
        status=AgentOperationStatus.RUNNING,
    )
    workflow = Workflow(
        id="workflow-1",
        goal_id="goal-1",
        step_ids=("step-1",),
        status=WorkflowStatus.COMPLETED,
    )

    updated = coordinator.complete(operation, goal, workflow)

    assert updated.status is AgentOperationStatus.COMPLETED


def test_complete_rejects_incomplete_workflow(
    coordinator: AgentOperationCoordinator,
    operation: AgentOperation,
    goal: Goal,
    workflow: Workflow,
) -> None:
    with pytest.raises(ValueError, match="workflow must be COMPLETED"):
        coordinator.complete(operation, goal, workflow)


def test_fail_accepts_failed_workflow(
    coordinator: AgentOperationCoordinator,
    goal: Goal,
) -> None:
    operation = AgentOperation(
        id="operation-1",
        goal_id="goal-1",
        workflow_id="workflow-1",
        status=AgentOperationStatus.RUNNING,
    )
    workflow = Workflow(
        id="workflow-1",
        goal_id="goal-1",
        step_ids=("step-1",),
        status=WorkflowStatus.FAILED,
    )

    updated = coordinator.fail(operation, goal, workflow)

    assert updated.status is AgentOperationStatus.FAILED


def test_fail_rejects_non_failed_workflow(
    coordinator: AgentOperationCoordinator,
    operation: AgentOperation,
    goal: Goal,
    workflow: Workflow,
) -> None:
    with pytest.raises(ValueError, match="workflow must be FAILED"):
        coordinator.fail(operation, goal, workflow)


def test_cancel_returns_cancelled_operation(
    coordinator: AgentOperationCoordinator,
    operation: AgentOperation,
    goal: Goal,
    workflow: Workflow,
) -> None:
    updated = coordinator.cancel(operation, goal, workflow)

    assert updated.status is AgentOperationStatus.CANCELLED
    assert operation.status is AgentOperationStatus.CREATED


def test_cancel_does_not_modify_goal_or_workflow(
    coordinator: AgentOperationCoordinator,
    operation: AgentOperation,
    goal: Goal,
    workflow: Workflow,
) -> None:
    coordinator.cancel(operation, goal, workflow)

    assert goal.status is GoalStatus.CREATED
    assert goal.progress == 0
    assert workflow.status is WorkflowStatus.READY


def test_pause_rejects_invalid_lifecycle_transition(
    coordinator: AgentOperationCoordinator,
    operation: AgentOperation,
    goal: Goal,
    workflow: Workflow,
) -> None:
    with pytest.raises(ValueError, match="Invalid operation status transition"):
        coordinator.pause(operation, goal, workflow)


def test_complete_rejects_invalid_lifecycle_transition(
    coordinator: AgentOperationCoordinator,
    goal: Goal,
) -> None:
    operation = AgentOperation(
        id="operation-1",
        goal_id="goal-1",
        workflow_id="workflow-1",
    )
    workflow = Workflow(
        id="workflow-1",
        goal_id="goal-1",
        step_ids=("step-1",),
        status=WorkflowStatus.COMPLETED,
    )

    with pytest.raises(ValueError, match="Invalid operation status transition"):
        coordinator.complete(operation, goal, workflow)