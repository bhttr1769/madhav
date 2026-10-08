import pytest

from brain.agents.models.agent_task import AgentTask
from brain.agents.models.agent_task_status import AgentTaskStatus
from brain.agents.models.workflow import Workflow
from brain.agents.models.workflow_step import (
    WorkflowStep,
    WorkflowStepStatus,
)
from brain.agents.workflow_task_integration import WorkflowTaskIntegration


def create_workflow(
    step_ids: tuple[str, ...] = ("step-1",),
) -> Workflow:
    return Workflow(
        id="workflow-1",
        goal_id="goal-1",
        step_ids=step_ids,
    )


def create_task(
    task_id: str,
    dependencies: frozenset[str] = frozenset(),
    status: AgentTaskStatus = AgentTaskStatus.CREATED,
) -> AgentTask:
    return AgentTask(
        id=task_id,
        goal_id="goal-1",
        description=f"Task {task_id}",
        dependencies=dependencies,
        status=status,
        progress=100 if status is AgentTaskStatus.COMPLETED else 0,
    )


def create_step(
    step_id: str,
    task_id: str,
    status: WorkflowStepStatus = WorkflowStepStatus.PENDING,
) -> WorkflowStep:
    return WorkflowStep(
        id=step_id,
        task_id=task_id,
        status=status,
    )


def test_task_without_dependencies_is_ready():
    integration = WorkflowTaskIntegration()

    workflow = create_workflow()
    steps = (create_step("step-1", "task-1"),)
    tasks = (create_task("task-1"),)

    ready = integration.ready_steps(
        workflow,
        steps,
        tasks,
    )

    assert ready == steps


def test_task_is_not_ready_when_dependency_is_incomplete():
    integration = WorkflowTaskIntegration()

    workflow = create_workflow()
    steps = (create_step("step-1", "task-2"),)

    tasks = (
        create_task("task-1"),
        create_task(
            "task-2",
            dependencies=frozenset({"task-1"}),
        ),
    )

    ready = integration.ready_steps(
        workflow,
        steps,
        tasks,
    )

    assert ready == ()


def test_task_is_ready_when_all_dependencies_are_completed():
    integration = WorkflowTaskIntegration()

    workflow = create_workflow()
    steps = (create_step("step-1", "task-3"),)

    tasks = (
        create_task(
            "task-1",
            status=AgentTaskStatus.COMPLETED,
        ),
        create_task(
            "task-2",
            status=AgentTaskStatus.COMPLETED,
        ),
        create_task(
            "task-3",
            dependencies=frozenset({"task-1", "task-2"}),
        ),
    )

    ready = integration.ready_steps(
        workflow,
        steps,
        tasks,
    )

    assert ready == steps


def test_completed_step_is_not_returned_as_ready():
    integration = WorkflowTaskIntegration()

    workflow = create_workflow()
    steps = (
        create_step(
            "step-1",
            "task-1",
            status=WorkflowStepStatus.COMPLETED,
        ),
    )
    tasks = (create_task("task-1"),)

    ready = integration.ready_steps(
        workflow,
        steps,
        tasks,
    )

    assert ready == ()


def test_running_step_is_not_returned_as_ready():
    integration = WorkflowTaskIntegration()

    workflow = create_workflow()
    steps = (
        create_step(
            "step-1",
            "task-1",
            status=WorkflowStepStatus.RUNNING,
        ),
    )
    tasks = (create_task("task-1"),)

    ready = integration.ready_steps(
        workflow,
        steps,
        tasks,
    )

    assert ready == ()


def test_rejects_unknown_step_task():
    integration = WorkflowTaskIntegration()

    workflow = create_workflow()
    steps = (create_step("step-1", "unknown-task"),)
    tasks = ()

    with pytest.raises(ValueError):
        integration.validate(
            workflow,
            steps,
            tasks,
        )


def test_rejects_unknown_dependency():
    integration = WorkflowTaskIntegration()

    workflow = create_workflow()
    steps = (create_step("step-1", "task-1"),)

    tasks = (
        create_task(
            "task-1",
            dependencies=frozenset({"unknown-task"}),
        ),
    )

    with pytest.raises(ValueError):
        integration.validate(
            workflow,
            steps,
            tasks,
        )


def test_rejects_task_from_different_goal():
    integration = WorkflowTaskIntegration()

    workflow = create_workflow()
    steps = (create_step("step-1", "task-1"),)

    tasks = (
        AgentTask(
            id="task-1",
            goal_id="different-goal",
            description="Task",
        ),
    )

    with pytest.raises(ValueError):
        integration.validate(
            workflow,
            steps,
            tasks,
        )


def test_does_not_modify_steps():
    integration = WorkflowTaskIntegration()

    workflow = create_workflow()
    steps = (create_step("step-1", "task-1"),)
    tasks = (create_task("task-1"),)

    integration.ready_steps(
        workflow,
        steps,
        tasks,
    )

    assert steps[0].status is WorkflowStepStatus.PENDING


def test_does_not_modify_tasks():
    integration = WorkflowTaskIntegration()

    workflow = create_workflow()
    steps = (create_step("step-1", "task-1"),)
    tasks = (create_task("task-1"),)

    integration.ready_steps(
        workflow,
        steps,
        tasks,
    )

    assert tasks[0].status is AgentTaskStatus.CREATED