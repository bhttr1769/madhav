import pytest

from brain.agents.models.agent_plan import AgentPlan


def test_creates_valid_agent_plan() -> None:
    plan = AgentPlan(
        goal_id="goal-1",
        task_order=("task-1", "task-2"),
        strategy=("Complete task-1 first", "Then complete task-2"),
        confidence=0.9,
    )

    assert plan.goal_id == "goal-1"
    assert plan.task_order == ("task-1", "task-2")
    assert plan.strategy == (
        "Complete task-1 first",
        "Then complete task-2",
    )
    assert plan.confidence == 0.9


def test_creates_plan_with_no_tasks() -> None:
    plan = AgentPlan(
        goal_id="goal-1",
        task_order=(),
        strategy=("No tasks are currently required",),
        confidence=0.5,
    )

    assert plan.task_order == ()


def test_creates_plan_with_empty_strategy() -> None:
    plan = AgentPlan(
        goal_id="goal-1",
        task_order=("task-1",),
        strategy=(),
        confidence=0.5,
    )

    assert plan.strategy == ()


def test_rejects_empty_goal_id() -> None:
    with pytest.raises(ValueError, match="goal_id"):
        AgentPlan(
            goal_id="",
            task_order=(),
            strategy=(),
            confidence=0.5,
        )


def test_rejects_non_string_goal_id() -> None:
    with pytest.raises(TypeError, match="goal_id"):
        AgentPlan(
            goal_id=123,
            task_order=(),
            strategy=(),
            confidence=0.5,
        )


def test_rejects_non_tuple_task_order() -> None:
    with pytest.raises(TypeError, match="task_order"):
        AgentPlan(
            goal_id="goal-1",
            task_order=["task-1"],
            strategy=(),
            confidence=0.5,
        )


def test_rejects_empty_task_id() -> None:
    with pytest.raises(ValueError, match="task_order"):
        AgentPlan(
            goal_id="goal-1",
            task_order=("task-1", ""),
            strategy=(),
            confidence=0.5,
        )


def test_rejects_non_string_task_id() -> None:
    with pytest.raises(TypeError, match="task_order"):
        AgentPlan(
            goal_id="goal-1",
            task_order=("task-1", 123),
            strategy=(),
            confidence=0.5,
        )


def test_rejects_duplicate_task_ids() -> None:
    with pytest.raises(
        ValueError,
        match="duplicate task IDs",
    ):
        AgentPlan(
            goal_id="goal-1",
            task_order=("task-1", "task-2", "task-1"),
            strategy=(),
            confidence=0.5,
        )


def test_rejects_non_tuple_strategy() -> None:
    with pytest.raises(TypeError, match="strategy"):
        AgentPlan(
            goal_id="goal-1",
            task_order=(),
            strategy=["step-1"],
            confidence=0.5,
        )


def test_rejects_empty_strategy_entry() -> None:
    with pytest.raises(ValueError, match="strategy"):
        AgentPlan(
            goal_id="goal-1",
            task_order=(),
            strategy=("step-1", ""),
            confidence=0.5,
        )


def test_rejects_non_string_strategy_entry() -> None:
    with pytest.raises(TypeError, match="strategy"):
        AgentPlan(
            goal_id="goal-1",
            task_order=(),
            strategy=("step-1", 123),
            confidence=0.5,
        )


def test_accepts_confidence_boundaries() -> None:
    low = AgentPlan(
        goal_id="goal-1",
        task_order=(),
        strategy=(),
        confidence=0.0,
    )

    high = AgentPlan(
        goal_id="goal-1",
        task_order=(),
        strategy=(),
        confidence=1.0,
    )

    assert low.confidence == 0.0
    assert high.confidence == 1.0


def test_rejects_confidence_below_zero() -> None:
    with pytest.raises(ValueError, match="confidence"):
        AgentPlan(
            goal_id="goal-1",
            task_order=(),
            strategy=(),
            confidence=-0.01,
        )


def test_rejects_confidence_above_one() -> None:
    with pytest.raises(ValueError, match="confidence"):
        AgentPlan(
            goal_id="goal-1",
            task_order=(),
            strategy=(),
            confidence=1.01,
        )


def test_rejects_non_numeric_confidence() -> None:
    with pytest.raises(TypeError, match="confidence"):
        AgentPlan(
            goal_id="goal-1",
            task_order=(),
            strategy=(),
            confidence="0.9",
        )


def test_rejects_boolean_confidence() -> None:
    with pytest.raises(TypeError, match="confidence"):
        AgentPlan(
            goal_id="goal-1",
            task_order=(),
            strategy=(),
            confidence=True,
        )


def test_agent_plan_is_immutable() -> None:
    plan = AgentPlan(
        goal_id="goal-1",
        task_order=("task-1",),
        strategy=("Complete task-1",),
        confidence=0.9,
    )

    with pytest.raises(AttributeError):
        plan.goal_id = "goal-2"