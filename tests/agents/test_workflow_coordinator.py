import pytest

from brain.agents.models.workflow import (
    Workflow,
    WorkflowStatus,
)
from brain.agents.models.workflow_step import (
    WorkflowStep,
    WorkflowStepStatus,
)
from brain.agents.workflow_coordinator import WorkflowCoordinator


def create_workflow(
    status: WorkflowStatus = WorkflowStatus.CREATED,
) -> Workflow:
    return Workflow(
        id="workflow-1",
        goal_id="goal-1",
        step_ids=(
            "step-1",
            "step-2",
        ),
        status=status,
    )


def create_steps() -> tuple[WorkflowStep, ...]:
    return (
        WorkflowStep(
            id="step-1",
            task_id="task-1",
        ),
        WorkflowStep(
            id="step-2",
            task_id="task-2",
        ),
    )


def test_start_transitions_workflow_to_running() -> None:
    coordinator = WorkflowCoordinator()

    workflow = create_workflow()
    steps = create_steps()

    updated_workflow, updated_steps = coordinator.start(
        workflow,
        steps,
    )

    assert updated_workflow.status is WorkflowStatus.RUNNING

    assert all(
        step.status is WorkflowStepStatus.READY
        for step in updated_steps
    )


def test_start_does_not_modify_original_objects() -> None:
    coordinator = WorkflowCoordinator()

    workflow = create_workflow()
    steps = create_steps()

    updated_workflow, updated_steps = coordinator.start(
        workflow,
        steps,
    )

    assert workflow.status is WorkflowStatus.CREATED

    assert all(
        step.status is WorkflowStepStatus.PENDING
        for step in steps
    )

    assert updated_workflow is not workflow
    assert updated_steps != steps


def test_start_rejects_non_matching_steps() -> None:
    coordinator = WorkflowCoordinator()

    workflow = create_workflow()

    steps = (
        WorkflowStep(
            id="unknown-step",
            task_id="task-1",
        ),
    )

    with pytest.raises(
        ValueError,
        match="do not match",
    ):
        coordinator.start(
            workflow,
            steps,
        )


def test_start_rejects_non_tuple_steps() -> None:
    coordinator = WorkflowCoordinator()

    with pytest.raises(
        TypeError,
        match="steps",
    ):
        coordinator.start(
            create_workflow(),
            [],
        )


def test_start_step_transitions_ready_step_to_running() -> None:
    coordinator = WorkflowCoordinator()

    workflow, steps = coordinator.start(
        create_workflow(),
        create_steps(),
    )

    updated_workflow, updated_steps = (
        coordinator.start_step(
            workflow,
            steps,
            "step-1",
        )
    )

    assert updated_workflow is workflow

    assert updated_steps[0].status is (
        WorkflowStepStatus.RUNNING
    )

    assert updated_steps[1].status is (
        WorkflowStepStatus.READY
    )

    assert steps[0].status is (
        WorkflowStepStatus.READY
    )


def test_start_step_requires_running_workflow() -> None:
    coordinator = WorkflowCoordinator()

    workflow = create_workflow(
        WorkflowStatus.READY,
    )

    steps = (
        WorkflowStep(
            id="step-1",
            task_id="task-1",
            status=WorkflowStepStatus.READY,
        ),
        WorkflowStep(
            id="step-2",
            task_id="task-2",
            status=WorkflowStepStatus.READY,
        ),
    )

    with pytest.raises(
        ValueError,
        match="workflow must be RUNNING",
    ):
        coordinator.start_step(
            workflow,
            steps,
            "step-1",
        )


def test_complete_step_updates_step() -> None:
    coordinator = WorkflowCoordinator()

    workflow, steps = coordinator.start(
        create_workflow(),
        create_steps(),
    )

    workflow, steps = coordinator.start_step(
        workflow,
        steps,
        "step-1",
    )

    updated_workflow, updated_steps = (
        coordinator.complete_step(
            workflow,
            steps,
            "step-1",
        )
    )

    assert updated_workflow.status is WorkflowStatus.RUNNING

    assert updated_steps[0].status is (
        WorkflowStepStatus.COMPLETED
    )

    assert updated_steps[1].status is (
        WorkflowStepStatus.READY
    )


def test_completing_last_step_completes_workflow() -> None:
    coordinator = WorkflowCoordinator()

    workflow, steps = coordinator.start(
        create_workflow(),
        create_steps(),
    )

    workflow, steps = coordinator.start_step(
        workflow,
        steps,
        "step-1",
    )

    workflow, steps = coordinator.complete_step(
        workflow,
        steps,
        "step-1",
    )

    workflow, steps = coordinator.start_step(
        workflow,
        steps,
        "step-2",
    )

    workflow, steps = coordinator.complete_step(
        workflow,
        steps,
        "step-2",
    )

    assert workflow.status is WorkflowStatus.COMPLETED

    assert all(
        step.status is WorkflowStepStatus.COMPLETED
        for step in steps
    )


def test_fail_step_fails_workflow() -> None:
    coordinator = WorkflowCoordinator()

    workflow, steps = coordinator.start(
        create_workflow(),
        create_steps(),
    )

    workflow, steps = coordinator.start_step(
        workflow,
        steps,
        "step-1",
    )

    workflow, steps = coordinator.fail_step(
        workflow,
        steps,
        "step-1",
    )

    assert workflow.status is WorkflowStatus.FAILED
    assert steps[0].status is WorkflowStepStatus.FAILED


def test_rejects_unknown_step() -> None:
    coordinator = WorkflowCoordinator()

    workflow, steps = coordinator.start(
        create_workflow(),
        create_steps(),
    )

    with pytest.raises(
        ValueError,
        match="Workflow step not found",
    ):
        coordinator.complete_step(
            workflow,
            steps,
            "unknown-step",
        )


def test_rejects_invalid_step_id() -> None:
    coordinator = WorkflowCoordinator()

    workflow, steps = coordinator.start(
        create_workflow(),
        create_steps(),
    )

    with pytest.raises(
        ValueError,
        match="step_id",
    ):
        coordinator.complete_step(
            workflow,
            steps,
            "   ",
        )


def test_rejects_duplicate_steps() -> None:
    coordinator = WorkflowCoordinator()

    workflow = create_workflow()

    steps = (
        WorkflowStep(
            id="step-1",
            task_id="task-1",
        ),
        WorkflowStep(
            id="step-1",
            task_id="task-2",
        ),
    )

    with pytest.raises(
        ValueError,
        match="duplicate",
    ):
        coordinator.start(
            workflow,
            steps,
        )