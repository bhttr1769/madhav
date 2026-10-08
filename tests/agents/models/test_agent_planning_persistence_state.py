import pytest

from brain.agents.models.agent_assignment import AgentAssignment
from brain.agents.models.agent_plan import AgentPlan
from brain.agents.models.agent_planning_persistence_state import (
    AgentPlanningPersistenceState,
)


def create_plan() -> AgentPlan:
    return AgentPlan(
        goal_id="goal-1",
        task_order=("task-1", "task-2"),
        strategy=("Complete task-1", "Complete task-2"),
        confidence=0.9,
    )


def create_assignments() -> tuple[AgentAssignment, ...]:
    return (
        AgentAssignment(
            task_id="task-1",
            agent_id="agent-1",
        ),
        AgentAssignment(
            task_id="task-2",
            agent_id="agent-2",
        ),
    )


def test_creates_valid_persistence_state() -> None:
    state = AgentPlanningPersistenceState(
        plan=create_plan(),
        assignments=create_assignments(),
    )

    assert state.plan == create_plan()
    assert state.assignments == create_assignments()


def test_allows_empty_assignments() -> None:
    state = AgentPlanningPersistenceState(
        plan=create_plan(),
        assignments=(),
    )

    assert state.assignments == ()


def test_rejects_invalid_plan() -> None:
    with pytest.raises(TypeError, match="plan"):
        AgentPlanningPersistenceState(
            plan="invalid",
            assignments=(),
        )


def test_rejects_non_tuple_assignments() -> None:
    with pytest.raises(TypeError, match="assignments"):
        AgentPlanningPersistenceState(
            plan=create_plan(),
            assignments=[],
        )


def test_rejects_invalid_assignment_entries() -> None:
    with pytest.raises(
        TypeError,
        match="AgentAssignment",
    ):
        AgentPlanningPersistenceState(
            plan=create_plan(),
            assignments=("invalid",),
        )


def test_persistence_state_is_immutable() -> None:
    state = AgentPlanningPersistenceState(
        plan=create_plan(),
        assignments=create_assignments(),
    )

    with pytest.raises(AttributeError):
        state.plan = create_plan()

def test_preserves_complete_planning_and_delegation_state() -> None:
    plan = AgentPlan(
        goal_id="goal-1",
        task_order=("task-1", "task-2"),
        strategy=(
            "Complete task-1",
            "Complete task-2",
        ),
        confidence=0.9,
    )

    assignments = (
        AgentAssignment(
            task_id="task-1",
            agent_id="agent-1",
        ),
        AgentAssignment(
            task_id="task-2",
            agent_id="agent-2",
        ),
    )

    state = AgentPlanningPersistenceState(
        plan=plan,
        assignments=assignments,
    )

    assert state.plan.goal_id == "goal-1"
    assert state.plan.task_order == (
        "task-1",
        "task-2",
    )
    assert state.assignments == assignments