import pytest

from brain.agents.models.agent_task import AgentTask
from brain.agents.models.goal import Goal
from brain.agents.models.goal_task_persistence_state import (
    GoalTaskPersistenceState,
)


def create_goal(
    goal_id="goal-1",
    agent_id="agent-1",
):
    return Goal(
        id=goal_id,
        agent_id=agent_id,
        description="Prepare the project",
    )


def create_task(
    task_id="task-1",
    goal_id="goal-1",
):
    return AgentTask(
        id=task_id,
        goal_id=goal_id,
        description="Inspect the repository",
    )


def test_goal_task_persistence_state_stores_data():
    goal = create_goal()
    task = create_task()

    state = GoalTaskPersistenceState(
        agent_id="agent-1",
        goals=(goal,),
        tasks=(task,),
    )

    assert state.agent_id == "agent-1"
    assert state.goals == (goal,)
    assert state.tasks == (task,)


def test_goal_task_persistence_state_is_immutable():
    state = GoalTaskPersistenceState(
        agent_id="agent-1",
        goals=(),
        tasks=(),
    )

    with pytest.raises(AttributeError):
        state.agent_id = "agent-2"


def test_goal_task_persistence_state_rejects_non_string_agent_id():
    with pytest.raises(TypeError):
        GoalTaskPersistenceState(
            agent_id=123,
            goals=(),
            tasks=(),
        )


def test_goal_task_persistence_state_rejects_empty_agent_id():
    with pytest.raises(ValueError):
        GoalTaskPersistenceState(
            agent_id="   ",
            goals=(),
            tasks=(),
        )


def test_goal_task_persistence_state_rejects_non_tuple_goals():
    with pytest.raises(TypeError):
        GoalTaskPersistenceState(
            agent_id="agent-1",
            goals=[],
            tasks=(),
        )


def test_goal_task_persistence_state_rejects_non_tuple_tasks():
    with pytest.raises(TypeError):
        GoalTaskPersistenceState(
            agent_id="agent-1",
            goals=(),
            tasks=[],
        )


def test_goal_task_persistence_state_rejects_invalid_goal():
    with pytest.raises(TypeError):
        GoalTaskPersistenceState(
            agent_id="agent-1",
            goals=("invalid",),
            tasks=(),
        )


def test_goal_task_persistence_state_rejects_invalid_task():
    with pytest.raises(TypeError):
        GoalTaskPersistenceState(
            agent_id="agent-1",
            goals=(),
            tasks=("invalid",),
        )


def test_goal_task_persistence_state_rejects_goal_owned_by_another_agent():
    goal = create_goal(agent_id="agent-2")

    with pytest.raises(ValueError):
        GoalTaskPersistenceState(
            agent_id="agent-1",
            goals=(goal,),
            tasks=(),
        )


def test_goal_task_persistence_state_rejects_task_with_unknown_goal():
    task = create_task(goal_id="unknown-goal")

    with pytest.raises(ValueError):
        GoalTaskPersistenceState(
            agent_id="agent-1",
            goals=(),
            tasks=(task,),
        )


def test_goal_task_persistence_state_rejects_duplicate_goal_ids():
    first = create_goal()
    second = create_goal()

    with pytest.raises(ValueError):
        GoalTaskPersistenceState(
            agent_id="agent-1",
            goals=(first, second),
            tasks=(),
        )


def test_goal_task_persistence_state_rejects_duplicate_task_ids():
    goal = create_goal()
    first = create_task()
    second = create_task()

    with pytest.raises(ValueError):
        GoalTaskPersistenceState(
            agent_id="agent-1",
            goals=(goal,),
            tasks=(first, second),
        )