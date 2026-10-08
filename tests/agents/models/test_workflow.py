import pytest

from brain.agents.models.workflow import (
    Workflow,
    WorkflowStatus,
)


def create_workflow() -> Workflow:
    return Workflow(
        id="workflow-1",
        goal_id="goal-1",
        step_ids=(
            "step-1",
            "step-2",
        ),
    )


def test_creates_valid_workflow() -> None:
    workflow = create_workflow()

    assert workflow.id == "workflow-1"
    assert workflow.goal_id == "goal-1"
    assert workflow.step_ids == (
        "step-1",
        "step-2",
    )
    assert workflow.status is WorkflowStatus.CREATED


def test_supports_all_workflow_statuses() -> None:
    assert set(WorkflowStatus) == {
        WorkflowStatus.CREATED,
        WorkflowStatus.READY,
        WorkflowStatus.RUNNING,
        WorkflowStatus.COMPLETED,
        WorkflowStatus.FAILED,
    }


@pytest.mark.parametrize(
    "workflow_id",
    [
        "",
        "   ",
        None,
        123,
    ],
)
def test_rejects_invalid_workflow_id(
    workflow_id: object,
) -> None:
    with pytest.raises((TypeError, ValueError)):
        Workflow(
            id=workflow_id,
            goal_id="goal-1",
            step_ids=(),
        )


@pytest.mark.parametrize(
    "goal_id",
    [
        "",
        "   ",
        None,
        123,
    ],
)
def test_rejects_invalid_goal_id(
    goal_id: object,
) -> None:
    with pytest.raises((TypeError, ValueError)):
        Workflow(
            id="workflow-1",
            goal_id=goal_id,
            step_ids=(),
        )


def test_rejects_non_tuple_step_ids() -> None:
    with pytest.raises(
        TypeError,
        match="step_ids",
    ):
        Workflow(
            id="workflow-1",
            goal_id="goal-1",
            step_ids=[],
        )


def test_rejects_invalid_step_id_entries() -> None:
    with pytest.raises(
        TypeError,
        match="step_ids",
    ):
        Workflow(
            id="workflow-1",
            goal_id="goal-1",
            step_ids=(123,),
        )


def test_rejects_empty_step_id() -> None:
    with pytest.raises(
        ValueError,
        match="step_ids",
    ):
        Workflow(
            id="workflow-1",
            goal_id="goal-1",
            step_ids=("",),
        )


def test_rejects_duplicate_step_ids() -> None:
    with pytest.raises(
        ValueError,
        match="duplicate",
    ):
        Workflow(
            id="workflow-1",
            goal_id="goal-1",
            step_ids=(
                "step-1",
                "step-1",
            ),
        )


def test_rejects_invalid_status() -> None:
    with pytest.raises(
        TypeError,
        match="status",
    ):
        Workflow(
            id="workflow-1",
            goal_id="goal-1",
            step_ids=(),
            status="created",
        )


def test_workflow_is_immutable() -> None:
    workflow = create_workflow()

    with pytest.raises(AttributeError):
        workflow.id = "workflow-2"


def test_workflow_allows_empty_steps() -> None:
    workflow = Workflow(
        id="workflow-1",
        goal_id="goal-1",
        step_ids=(),
    )

    assert workflow.step_ids == ()