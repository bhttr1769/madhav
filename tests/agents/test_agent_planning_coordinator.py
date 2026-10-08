from unittest.mock import Mock

import pytest

from brain.agents.agent_planning_coordinator import (
    AgentPlanningCoordinator,
    AgentPlanningResult,
)
from brain.agents.agent_selector import AgentSelector
from brain.agents.models.agent_assignment import AgentAssignment
from brain.agents.models.agent_plan import AgentPlan
from brain.agents.models.agent_task import AgentTask
from brain.agents.models.goal import Goal
from brain.agents.planning.agent_planner import AgentPlanner


def create_goal() -> Goal:
    return Goal(
        id="goal-1",
        agent_id="agent-owner",
        description="Complete the goal",
    )


def create_task(task_id: str) -> AgentTask:
    return AgentTask(
        id=task_id,
        goal_id="goal-1",
        description=f"Complete {task_id}",
    )


def create_plan() -> AgentPlan:
    return AgentPlan(
        goal_id="goal-1",
        task_order=("task-1", "task-2"),
        strategy=("Complete task-1", "Complete task-2"),
        confidence=0.9,
    )


def create_single_task_plan() -> AgentPlan:
    return AgentPlan(
        goal_id="goal-1",
        task_order=("task-1",),
        strategy=("Complete task-1",),
        confidence=0.9,
    )


def create_coordinator(
    plan: AgentPlan | None = None,
) -> tuple[
    AgentPlanningCoordinator,
    Mock,
    Mock,
]:
    planner = Mock(spec=AgentPlanner)
    selector = Mock(spec=AgentSelector)

    planner.plan.return_value = (
        plan if plan is not None else create_plan()
    )

    def delegate(
        task: AgentTask,
        _required_capabilities: frozenset[str],
    ) -> AgentAssignment:
        return AgentAssignment(
            task_id=task.id,
            agent_id=f"agent-for-{task.id}",
        )

    selector.delegate.side_effect = delegate

    coordinator = AgentPlanningCoordinator(
        planner=planner,
        selector=selector,
    )

    return coordinator, planner, selector


def test_plan_and_delegate_returns_result() -> None:
    coordinator, planner, selector = create_coordinator()

    goal = create_goal()
    tasks = (
        create_task("task-1"),
        create_task("task-2"),
    )

    result = coordinator.plan_and_delegate(
        goal=goal,
        tasks=tasks,
        required_capabilities_by_task={
            "task-1": frozenset({"coding"}),
            "task-2": frozenset({"testing"}),
        },
    )

    assert isinstance(result, AgentPlanningResult)
    assert result.plan == create_plan()

    assert result.assignments == (
        AgentAssignment(
            task_id="task-1",
            agent_id="agent-for-task-1",
        ),
        AgentAssignment(
            task_id="task-2",
            agent_id="agent-for-task-2",
        ),
    )

    planner.plan.assert_called_once_with(
        goal,
        tasks,
    )

    assert selector.delegate.call_count == 2


def test_delegates_tasks_in_plan_order() -> None:
    plan = AgentPlan(
        goal_id="goal-1",
        task_order=("task-2", "task-1"),
        strategy=("Complete task-2 first",),
        confidence=0.8,
    )

    coordinator, _, selector = create_coordinator(plan)

    task_1 = create_task("task-1")
    task_2 = create_task("task-2")

    coordinator.plan_and_delegate(
        goal=create_goal(),
        tasks=(task_1, task_2),
        required_capabilities_by_task={
            "task-1": frozenset({"coding"}),
            "task-2": frozenset({"testing"}),
        },
    )

    calls = selector.delegate.call_args_list

    assert calls[0].args == (
        task_2,
        frozenset({"testing"}),
    )

    assert calls[1].args == (
        task_1,
        frozenset({"coding"}),
    )


def test_uses_empty_capabilities_when_requirement_is_missing() -> None:
    coordinator, _, selector = create_coordinator(
        create_single_task_plan(),
    )

    task = create_task("task-1")

    coordinator.plan_and_delegate(
        goal=create_goal(),
        tasks=(task,),
        required_capabilities_by_task={},
    )

    selector.delegate.assert_called_once_with(
        task,
        frozenset(),
    )


def test_rejects_unknown_task_referenced_by_plan() -> None:
    plan = AgentPlan(
        goal_id="goal-1",
        task_order=("unknown-task",),
        strategy=(),
        confidence=0.5,
    )

    coordinator, _, _ = create_coordinator(plan)

    with pytest.raises(
        ValueError,
        match="unknown task",
    ):
        coordinator.plan_and_delegate(
            goal=create_goal(),
            tasks=(create_task("task-1"),),
            required_capabilities_by_task={},
        )


def test_rejects_non_tuple_tasks() -> None:
    coordinator, _, _ = create_coordinator()

    with pytest.raises(TypeError, match="tasks"):
        coordinator.plan_and_delegate(
            goal=create_goal(),
            tasks=[create_task("task-1")],
            required_capabilities_by_task={},
        )


def test_rejects_invalid_task_entries() -> None:
    coordinator, _, _ = create_coordinator()

    with pytest.raises(
        TypeError,
        match="AgentTask",
    ):
        coordinator.plan_and_delegate(
            goal=create_goal(),
            tasks=("task-1",),
            required_capabilities_by_task={},
        )


def test_rejects_invalid_capability_mapping() -> None:
    coordinator, _, _ = create_coordinator()

    with pytest.raises(
        TypeError,
        match="must be a dict",
    ):
        coordinator.plan_and_delegate(
            goal=create_goal(),
            tasks=(create_task("task-1"),),
            required_capabilities_by_task=[],
        )


def test_rejects_non_string_task_mapping_key() -> None:
    coordinator, _, _ = create_coordinator()

    with pytest.raises(
        TypeError,
        match="keys must be strings",
    ):
        coordinator.plan_and_delegate(
            goal=create_goal(),
            tasks=(create_task("task-1"),),
            required_capabilities_by_task={
                123: frozenset({"coding"}),
            },
        )


def test_rejects_non_frozenset_capability_requirement() -> None:
    coordinator, _, _ = create_coordinator()

    with pytest.raises(
        TypeError,
        match="must be frozensets",
    ):
        coordinator.plan_and_delegate(
            goal=create_goal(),
            tasks=(create_task("task-1"),),
            required_capabilities_by_task={
                "task-1": {"coding"},
            },
        )


def test_does_not_modify_tasks() -> None:
    coordinator, _, _ = create_coordinator(
        create_single_task_plan(),
    )

    task = create_task("task-1")

    coordinator.plan_and_delegate(
        goal=create_goal(),
        tasks=(task,),
        required_capabilities_by_task={
            "task-1": frozenset({"coding"}),
        },
    )

    assert task.id == "task-1"
    assert task.goal_id == "goal-1"
    assert task.description == "Complete task-1"


def test_does_not_execute_tasks() -> None:
    coordinator, planner, selector = create_coordinator(
        create_single_task_plan(),
    )

    task = create_task("task-1")

    coordinator.plan_and_delegate(
        goal=create_goal(),
        tasks=(task,),
        required_capabilities_by_task={
            "task-1": frozenset({"coding"}),
        },
    )

    planner.plan.assert_called_once()
    selector.delegate.assert_called_once()

    assert task.id == "task-1"