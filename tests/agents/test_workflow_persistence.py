import pytest

from brain.agents.models.workflow import (
    Workflow,
    WorkflowStatus,
)
from brain.agents.models.workflow_persistence_state import (
    WorkflowPersistenceState,
)
from brain.agents.models.workflow_step import (
    WorkflowStep,
    WorkflowStepStatus,
)
from brain.agents.workflow_persistence import (
    WorkflowPersistence,
)


def create_workflow(
    step_ids: tuple[str, ...] = (
        "step-1",
        "step-2",
    ),
) -> Workflow:
    return Workflow(
        id="workflow-1",
        goal_id="goal-1",
        step_ids=step_ids,
        status=WorkflowStatus.RUNNING,
    )


def create_steps() -> tuple[WorkflowStep, ...]:
    return (
        WorkflowStep(
            id="step-1",
            task_id="task-1",
            status=WorkflowStepStatus.READY,
        ),
        WorkflowStep(
            id="step-2",
            task_id="task-2",
            status=WorkflowStepStatus.PENDING,
        ),
    )


class FakeWorkflowPersistence:
    def __init__(self) -> None:
        self.saved_state = None

    def save(
        self,
        state: WorkflowPersistenceState,
    ) -> None:
        self.saved_state = state

    def load(
        self,
        workflow_id: str,
    ) -> WorkflowPersistenceState:
        if self.saved_state is None:
            raise KeyError(workflow_id)

        if self.saved_state.workflow.id != workflow_id:
            raise KeyError(workflow_id)

        return self.saved_state


def test_persistence_state_accepts_valid_workflow_and_steps() -> None:
    workflow = create_workflow()
    steps = create_steps()

    state = WorkflowPersistenceState(
        workflow=workflow,
        steps=steps,
    )

    assert state.workflow is workflow
    assert state.steps == steps


def test_persistence_state_is_immutable() -> None:
    state = WorkflowPersistenceState(
        workflow=create_workflow(),
        steps=create_steps(),
    )

    with pytest.raises(AttributeError):
        state.workflow = create_workflow()


def test_persistence_state_rejects_invalid_workflow() -> None:
    with pytest.raises(TypeError, match="workflow"):
        WorkflowPersistenceState(
            workflow=object(),
            steps=create_steps(),
        )


def test_persistence_state_rejects_non_tuple_steps() -> None:
    with pytest.raises(TypeError, match="steps"):
        WorkflowPersistenceState(
            workflow=create_workflow(),
            steps=[],
        )


def test_persistence_state_rejects_invalid_step_type() -> None:
    with pytest.raises(
        TypeError,
        match="WorkflowStep",
    ):
        WorkflowPersistenceState(
            workflow=create_workflow(),
            steps=(
                object(),
            ),
        )


def test_persistence_state_rejects_duplicate_step_ids() -> None:
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
        match="unique",
    ):
        WorkflowPersistenceState(
            workflow=workflow,
            steps=steps,
        )


def test_persistence_state_rejects_non_matching_step_ids() -> None:
    workflow = create_workflow()

    steps = (
        WorkflowStep(
            id="step-1",
            task_id="task-1",
        ),
        WorkflowStep(
            id="unknown-step",
            task_id="task-2",
        ),
    )

    with pytest.raises(
        ValueError,
        match="do not match",
    ):
        WorkflowPersistenceState(
            workflow=workflow,
            steps=steps,
        )


def test_fake_persistence_saves_and_loads_state() -> None:
    persistence = FakeWorkflowPersistence()

    state = WorkflowPersistenceState(
        workflow=create_workflow(),
        steps=create_steps(),
    )

    persistence.save(state)

    restored = persistence.load("workflow-1")

    assert restored is state


def test_persistence_contract_can_be_implemented() -> None:
    persistence = FakeWorkflowPersistence()

    assert isinstance(
        persistence,
        WorkflowPersistence,
    )


def test_persistence_load_rejects_unknown_workflow() -> None:
    persistence = FakeWorkflowPersistence()

    state = WorkflowPersistenceState(
        workflow=create_workflow(),
        steps=create_steps(),
    )

    persistence.save(state)

    with pytest.raises(KeyError):
        persistence.load("unknown-workflow")