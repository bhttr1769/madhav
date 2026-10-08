import pytest

from brain.agents.models.workflow import WorkflowStatus
from brain.agents.models.workflow_step import WorkflowStepStatus
from brain.agents.workflow_lifecycle import WorkflowLifecycle


@pytest.mark.parametrize(
    "current,target",
    [
        (
            WorkflowStatus.CREATED,
            WorkflowStatus.READY,
        ),
        (
            WorkflowStatus.READY,
            WorkflowStatus.RUNNING,
        ),
        (
            WorkflowStatus.RUNNING,
            WorkflowStatus.COMPLETED,
        ),
        (
            WorkflowStatus.RUNNING,
            WorkflowStatus.FAILED,
        ),
    ],
)
def test_allows_valid_workflow_transitions(
    current: WorkflowStatus,
    target: WorkflowStatus,
) -> None:
    assert WorkflowLifecycle.can_transition_workflow(
        current,
        target,
    )


@pytest.mark.parametrize(
    "current,target",
    [
        (
            WorkflowStatus.CREATED,
            WorkflowStatus.RUNNING,
        ),
        (
            WorkflowStatus.CREATED,
            WorkflowStatus.COMPLETED,
        ),
        (
            WorkflowStatus.READY,
            WorkflowStatus.COMPLETED,
        ),
        (
            WorkflowStatus.COMPLETED,
            WorkflowStatus.RUNNING,
        ),
        (
            WorkflowStatus.FAILED,
            WorkflowStatus.READY,
        ),
    ],
)
def test_rejects_invalid_workflow_transitions(
    current: WorkflowStatus,
    target: WorkflowStatus,
) -> None:
    assert not WorkflowLifecycle.can_transition_workflow(
        current,
        target,
    )


def test_validates_workflow_transition() -> None:
    WorkflowLifecycle.validate_workflow_transition(
        WorkflowStatus.CREATED,
        WorkflowStatus.READY,
    )


def test_rejects_invalid_workflow_transition() -> None:
    with pytest.raises(
        ValueError,
        match="Invalid workflow transition",
    ):
        WorkflowLifecycle.validate_workflow_transition(
            WorkflowStatus.CREATED,
            WorkflowStatus.COMPLETED,
        )


@pytest.mark.parametrize(
    "current,target",
    [
        (
            WorkflowStepStatus.PENDING,
            WorkflowStepStatus.READY,
        ),
        (
            WorkflowStepStatus.READY,
            WorkflowStepStatus.RUNNING,
        ),
        (
            WorkflowStepStatus.RUNNING,
            WorkflowStepStatus.COMPLETED,
        ),
        (
            WorkflowStepStatus.RUNNING,
            WorkflowStepStatus.FAILED,
        ),
    ],
)
def test_allows_valid_step_transitions(
    current: WorkflowStepStatus,
    target: WorkflowStepStatus,
) -> None:
    assert WorkflowLifecycle.can_transition_step(
        current,
        target,
    )


@pytest.mark.parametrize(
    "current,target",
    [
        (
            WorkflowStepStatus.PENDING,
            WorkflowStepStatus.RUNNING,
        ),
        (
            WorkflowStepStatus.PENDING,
            WorkflowStepStatus.COMPLETED,
        ),
        (
            WorkflowStepStatus.READY,
            WorkflowStepStatus.COMPLETED,
        ),
        (
            WorkflowStepStatus.COMPLETED,
            WorkflowStepStatus.RUNNING,
        ),
        (
            WorkflowStepStatus.FAILED,
            WorkflowStepStatus.READY,
        ),
    ],
)
def test_rejects_invalid_step_transitions(
    current: WorkflowStepStatus,
    target: WorkflowStepStatus,
) -> None:
    assert not WorkflowLifecycle.can_transition_step(
        current,
        target,
    )


def test_validates_step_transition() -> None:
    WorkflowLifecycle.validate_step_transition(
        WorkflowStepStatus.PENDING,
        WorkflowStepStatus.READY,
    )


def test_rejects_invalid_step_transition() -> None:
    with pytest.raises(
        ValueError,
        match="Invalid workflow step transition",
    ):
        WorkflowLifecycle.validate_step_transition(
            WorkflowStepStatus.PENDING,
            WorkflowStepStatus.COMPLETED,
        )


def test_rejects_invalid_workflow_status() -> None:
    with pytest.raises(
        TypeError,
        match="WorkflowStatus",
    ):
        WorkflowLifecycle.can_transition_workflow(
            "created",
            WorkflowStatus.READY,
        )


def test_rejects_invalid_step_status() -> None:
    with pytest.raises(
        TypeError,
        match="WorkflowStepStatus",
    ):
        WorkflowLifecycle.can_transition_step(
            "pending",
            WorkflowStepStatus.READY,
        )