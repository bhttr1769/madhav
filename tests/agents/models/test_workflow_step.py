import pytest

from brain.agents.models.workflow_step import (
    WorkflowStep,
    WorkflowStepStatus,
)


def create_step() -> WorkflowStep:
    return WorkflowStep(
        id="step-1",
        task_id="task-1",
    )


def test_creates_valid_workflow_step() -> None:
    step = create_step()

    assert step.id == "step-1"
    assert step.task_id == "task-1"
    assert step.status is WorkflowStepStatus.PENDING


def test_supports_all_workflow_step_statuses() -> None:
    assert set(WorkflowStepStatus) == {
        WorkflowStepStatus.PENDING,
        WorkflowStepStatus.READY,
        WorkflowStepStatus.RUNNING,
        WorkflowStepStatus.COMPLETED,
        WorkflowStepStatus.FAILED,
    }


@pytest.mark.parametrize(
    "step_id",
    [
        "",
        "   ",
        None,
        123,
    ],
)
def test_rejects_invalid_step_id(
    step_id: object,
) -> None:
    with pytest.raises((TypeError, ValueError)):
        WorkflowStep(
            id=step_id,
            task_id="task-1",
        )


@pytest.mark.parametrize(
    "task_id",
    [
        "",
        "   ",
        None,
        123,
    ],
)
def test_rejects_invalid_task_id(
    task_id: object,
) -> None:
    with pytest.raises((TypeError, ValueError)):
        WorkflowStep(
            id="step-1",
            task_id=task_id,
        )


def test_rejects_invalid_status() -> None:
    with pytest.raises(
        TypeError,
        match="status",
    ):
        WorkflowStep(
            id="step-1",
            task_id="task-1",
            status="pending",
        )


def test_workflow_step_is_immutable() -> None:
    step = create_step()

    with pytest.raises(AttributeError):
        step.id = "step-2"


def test_workflow_step_references_existing_task() -> None:
    step = WorkflowStep(
        id="step-1",
        task_id="existing-task",
    )

    assert step.task_id == "existing-task"