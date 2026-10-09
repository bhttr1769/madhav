import pytest

from brain.agents.agent_operation_workflow_coordinator import (
    AgentOperationWorkflowCoordinator,
)
from brain.agents.models.agent_operation import (
    AgentOperation,
    AgentOperationStatus,
)
from brain.agents.models.goal import Goal
from brain.agents.models.workflow import Workflow, WorkflowStatus
from brain.agents.models.workflow_step import (
    WorkflowStep,
    WorkflowStepStatus,
)
from unittest.mock import Mock

from brain.agents.models.agent_task import AgentTask
from brain.agents.models.agent_task_status import AgentTaskStatus



@pytest.fixture
def coordinator() -> AgentOperationWorkflowCoordinator:
    return AgentOperationWorkflowCoordinator()


@pytest.fixture
def goal() -> Goal:
    return Goal(
        id="goal-1",
        agent_id="agent-1",
        description="Complete assigned work",
    )


@pytest.fixture
def workflow() -> Workflow:
    return Workflow(
        id="workflow-1",
        goal_id="goal-1",
        step_ids=("step-1",),
        status=WorkflowStatus.RUNNING,
    )


@pytest.fixture
def operation() -> AgentOperation:
    return AgentOperation(
        id="operation-1",
        goal_id="goal-1",
        workflow_id="workflow-1",
        status=AgentOperationStatus.RUNNING,
    )


@pytest.fixture
def steps() -> tuple[WorkflowStep, ...]:
    return (
        WorkflowStep(
            id="step-1",
            task_id="task-1",
            status=WorkflowStepStatus.READY,
        ),
    )


def test_pause_preserves_workflow_and_steps(
    coordinator,
    operation,
    goal,
    workflow,
    steps,
):
    updated = coordinator.pause(operation, goal, workflow, steps)

    assert updated.status is AgentOperationStatus.PAUSED
    assert operation.status is AgentOperationStatus.RUNNING
    assert workflow.status is WorkflowStatus.RUNNING
    assert steps[0].status is WorkflowStepStatus.READY


def test_pause_rejects_running_step(
    coordinator,
    operation,
    goal,
    workflow,
):
    running_steps = (
        WorkflowStep(
            id="step-1",
            task_id="task-1",
            status=WorkflowStepStatus.RUNNING,
        ),
    )

    with pytest.raises(ValueError, match="no workflow step is RUNNING"):
        coordinator.pause(
            operation,
            goal,
            workflow,
            running_steps,
        )


def test_resume_returns_running_operation(
    coordinator,
    goal,
    workflow,
):
    paused = AgentOperation(
        id="operation-1",
        goal_id="goal-1",
        workflow_id="workflow-1",
        status=AgentOperationStatus.PAUSED,
    )

    updated = coordinator.resume(paused, goal, workflow)

    assert updated.status is AgentOperationStatus.RUNNING
    assert paused.status is AgentOperationStatus.PAUSED


def test_resume_rejects_non_paused_operation(
    coordinator,
    operation,
    goal,
    workflow,
):
    with pytest.raises(ValueError, match="operation must be PAUSED"):
        coordinator.resume(operation, goal, workflow)


def test_start_step_delegates_when_operation_is_running(
    coordinator,
    operation,
    goal,
    workflow,
    steps,
):
    updated_workflow, updated_steps = coordinator.start_step(
        operation,
        goal,
        workflow,
        steps,
        "step-1",
    )

    assert updated_workflow is workflow
    assert updated_steps[0].status is WorkflowStepStatus.RUNNING
    assert steps[0].status is WorkflowStepStatus.READY


def test_paused_operation_cannot_start_step(
    coordinator,
    goal,
    workflow,
    steps,
):
    paused = AgentOperation(
        id="operation-1",
        goal_id="goal-1",
        workflow_id="workflow-1",
        status=AgentOperationStatus.PAUSED,
    )

    with pytest.raises(ValueError, match="operation must be RUNNING"):
        coordinator.start_step(
            paused,
            goal,
            workflow,
            steps,
            "step-1",
        )


def test_paused_operation_cannot_complete_step(
    coordinator,
    goal,
    workflow,
    steps,
):
    paused = AgentOperation(
        id="operation-1",
        goal_id="goal-1",
        workflow_id="workflow-1",
        status=AgentOperationStatus.PAUSED,
    )

    with pytest.raises(ValueError, match="operation must be RUNNING"):
        coordinator.complete_step(
            paused,
            goal,
            workflow,
            steps,
            "step-1",
        )


def test_pause_rejects_non_running_workflow(
    coordinator,
    operation,
    goal,
    steps,
):
    ready_workflow = Workflow(
        id="workflow-1",
        goal_id="goal-1",
        step_ids=("step-1",),
        status=WorkflowStatus.READY,
    )

    with pytest.raises(ValueError, match="workflow must be RUNNING"):
        coordinator.pause(
            operation,
            goal,
            ready_workflow,
            steps,
        )

def test_fail_step_fails_both_operation_and_workflow(
    coordinator,
    operation,
    goal,
    workflow,
):
    running_steps = (
        WorkflowStep(
            id="step-1",
            task_id="task-1",
            status=WorkflowStepStatus.RUNNING,
        ),
    )

    updated_operation, updated_workflow, updated_steps = (
        coordinator.fail_step(
            operation,
            goal,
            workflow,
            running_steps,
            "step-1",
        )
    )

    assert updated_operation.status is AgentOperationStatus.FAILED
    assert updated_workflow.status is WorkflowStatus.FAILED
    assert updated_steps[0].status is WorkflowStepStatus.FAILED

    assert operation.status is AgentOperationStatus.RUNNING
    assert workflow.status is WorkflowStatus.RUNNING
    assert running_steps[0].status is WorkflowStepStatus.RUNNING

def test_fail_step_rejects_paused_operation(
    coordinator,
    goal,
    workflow,
    steps,
):
    paused_operation = AgentOperation(
        id="operation-1",
        goal_id="goal-1",
        workflow_id="workflow-1",
        status=AgentOperationStatus.PAUSED,
    )

    with pytest.raises(ValueError, match="operation must be RUNNING"):
        coordinator.fail_step(
            paused_operation,
            goal,
            workflow,
            steps,
            "step-1",
        )

@pytest.fixture
def runtime():
    runtime = Mock()
    runtime.agent_id = "agent-1"
    runtime.authorize_goal.return_value = None
    runtime.authorize_task.return_value = None
    return runtime


@pytest.fixture
def tasks():
    return (
        AgentTask(
            id="task-1",
            goal_id="goal-1",
            description="Complete assigned work",
            status=AgentTaskStatus.ACTIVE,
            progress=50,
        ),
    )


@pytest.fixture
def running_steps():
    return (
        WorkflowStep(
            id="step-1",
            task_id="task-1",
            status=WorkflowStepStatus.RUNNING,
        ),
    )

def test_start_task_step_activates_task(
    coordinator, operation, runtime, goal, workflow, steps
):
    tasks = (
        AgentTask(
            id="task-1",
            goal_id="goal-1",
            description="Complete assigned work",
            status=AgentTaskStatus.CREATED,
            progress=0,
        ),
    )

    updated_workflow, updated_steps, updated_tasks = (
        coordinator.start_task_step(
            operation, runtime, goal, workflow, steps, tasks, "step-1"
        )
    )

    assert updated_steps[0].status is WorkflowStepStatus.RUNNING
    assert updated_tasks[0].status is AgentTaskStatus.ACTIVE
    assert tasks[0].status is AgentTaskStatus.CREATED


def test_complete_task_step_completes_task(
    coordinator, operation, runtime, goal, workflow, running_steps, tasks
):
    updated_operation, updated_workflow, updated_steps, updated_tasks = (
        coordinator.complete_task_step(
            operation,
            runtime,
            goal,
            workflow,
            running_steps,
            tasks,
            "step-1",
        )
    )

    assert updated_tasks[0].status is AgentTaskStatus.COMPLETED
    assert updated_tasks[0].progress == 100
    assert updated_steps[0].status is WorkflowStepStatus.COMPLETED
    assert tasks[0].status is AgentTaskStatus.ACTIVE

def test_fail_task_step_fails_task_workflow_and_operation(
    coordinator, operation, runtime, goal, workflow, running_steps, tasks
):
    updated_operation, updated_workflow, updated_steps, updated_tasks = (
        coordinator.fail_task_step(
            operation,
            runtime,
            goal,
            workflow,
            running_steps,
            tasks,
            "step-1",
        )
    )

    assert updated_operation.status is AgentOperationStatus.FAILED
    assert updated_workflow.status is WorkflowStatus.FAILED
    assert updated_steps[0].status is WorkflowStepStatus.FAILED
    assert updated_tasks[0].status is AgentTaskStatus.FAILED
    assert tasks[0].status is AgentTaskStatus.ACTIVE

def test_start_task_step_rejects_unauthorized_goal(
    coordinator, operation, runtime, goal, workflow, steps, tasks
):
    runtime.authorize_goal.side_effect = ValueError("unauthorized")

    with pytest.raises(ValueError, match="unauthorized"):
        coordinator.start_task_step(
            operation, runtime, goal, workflow, steps, tasks, "step-1"
        )

    assert steps[0].status is WorkflowStepStatus.READY
    assert tasks[0].status is AgentTaskStatus.ACTIVE