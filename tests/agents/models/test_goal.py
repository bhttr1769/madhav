import pytest

from brain.agents.models.goal import Goal
from brain.agents.models.goal_status import GoalStatus


def test_goal_can_be_created():
    goal = Goal(
        id="goal-1",
        agent_id="agent-1",
        description="Prepare the project for release",
    )

    assert goal.id == "goal-1"
    assert goal.agent_id == "agent-1"
    assert goal.description == "Prepare the project for release"
    assert goal.status is GoalStatus.CREATED


def test_goal_accepts_explicit_status():
    goal = Goal(
        id="goal-1",
        agent_id="agent-1",
        description="Prepare the project for release",
        status=GoalStatus.ACTIVE,
    )

    assert goal.status is GoalStatus.ACTIVE


def test_goal_is_immutable():
    goal = Goal(
        id="goal-1",
        agent_id="agent-1",
        description="Prepare the project for release",
    )

    with pytest.raises(AttributeError):
        goal.description = "Changed"


@pytest.mark.parametrize("field", ["id", "agent_id", "description"])
def test_goal_rejects_non_string_required_fields(field):
    values = {
        "id": "goal-1",
        "agent_id": "agent-1",
        "description": "Prepare the project",
    }
    values[field] = 123

    with pytest.raises(TypeError):
        Goal(**values)


@pytest.mark.parametrize("field", ["id", "agent_id", "description"])
def test_goal_rejects_empty_required_fields(field):
    values = {
        "id": "goal-1",
        "agent_id": "agent-1",
        "description": "Prepare the project",
    }
    values[field] = "   "

    with pytest.raises(ValueError):
        Goal(**values)


def test_goal_rejects_invalid_status():
    with pytest.raises(TypeError):
        Goal(
            id="goal-1",
            agent_id="agent-1",
            description="Prepare the project",
            status="active",
        )


def test_goals_with_same_values_are_equal():
    first = Goal(
        id="goal-1",
        agent_id="agent-1",
        description="Prepare the project",
    )
    second = Goal(
        id="goal-1",
        agent_id="agent-1",
        description="Prepare the project",
    )

    assert first == second

def test_goal_defaults_to_zero_progress():
    goal = Goal(
        id="goal-1",
        agent_id="agent-1",
        description="Prepare the project",
    )

    assert goal.progress == 0


def test_goal_accepts_valid_progress():
    goal = Goal(
        id="goal-1",
        agent_id="agent-1",
        description="Prepare the project",
        status=GoalStatus.ACTIVE,
        progress=50,
    )

    assert goal.progress == 50


@pytest.mark.parametrize("progress", [-1, 101])
def test_goal_rejects_progress_outside_range(progress):
    with pytest.raises(ValueError):
        Goal(
            id="goal-1",
            agent_id="agent-1",
            description="Prepare the project",
            progress=progress,
        )


def test_goal_rejects_non_integer_progress():
    with pytest.raises(TypeError):
        Goal(
            id="goal-1",
            agent_id="agent-1",
            description="Prepare the project",
            progress=50.5,
        )


def test_goal_rejects_boolean_progress():
    with pytest.raises(TypeError):
        Goal(
            id="goal-1",
            agent_id="agent-1",
            description="Prepare the project",
            progress=True,
        )


def test_completed_goal_requires_full_progress():
    with pytest.raises(ValueError):
        Goal(
            id="goal-1",
            agent_id="agent-1",
            description="Prepare the project",
            status=GoalStatus.COMPLETED,
            progress=99,
        )


def test_completed_goal_accepts_full_progress():
    goal = Goal(
        id="goal-1",
        agent_id="agent-1",
        description="Prepare the project",
        status=GoalStatus.COMPLETED,
        progress=100,
    )

    assert goal.progress == 100

@pytest.mark.parametrize(
    "status",
    [
        GoalStatus.ACTIVE,
        GoalStatus.FAILED,
        GoalStatus.CANCELLED,
    ],
)
def test_non_completed_goal_rejects_full_progress(status):
    with pytest.raises(ValueError):
        Goal(
            id="goal-1",
            agent_id="agent-1",
            description="Prepare the project",
            status=status,
            progress=100,
        )


def test_created_goal_requires_zero_progress():
    with pytest.raises(ValueError):
        Goal(
            id="goal-1",
            agent_id="agent-1",
            description="Prepare the project",
            status=GoalStatus.CREATED,
            progress=1,
        )