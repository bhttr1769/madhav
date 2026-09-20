import pytest

from brain.engineering.loop.models.engineering_loop_result import (
    EngineeringLoopResult,
)
from brain.evolution.models.evolution_result import (
    EvolutionResult,
)
from brain.evolution.models.evolution_task_result import (
    EvolutionTaskResult,
)


def create_task_result(
    task_id: str,
    passed: bool,
    changes=(),
):
    engineering_result = EngineeringLoopResult(
        changes=(),
        passed=passed,
        iterations=(),
        termination_reason=(
            "verification_passed"
            if passed
            else "max_iterations_reached"
        ),
    )

    return EvolutionTaskResult(
        task_id=task_id,
        task_description=f"Task {task_id}",
        proposed_changes=changes,
        engineering_result=engineering_result,
    )


def create_evolution_result(
    task_results,
):
    return EvolutionResult(
        requested_capability="repository_analysis",
        requirement=None,
        task_decomposition=None,
        design=None,
        plan=None,
        task_results=task_results,
    )


def test_proposed_changes_are_aggregated():
    first_change = object()
    second_change = object()

    result = create_evolution_result(
        (
            create_task_result(
                "task-1",
                True,
                (first_change,),
            ),
            create_task_result(
                "task-2",
                True,
                (second_change,),
            ),
        )
    )

    assert result.all_proposed_changes == (
        first_change,
        second_change,
    )


def test_passed_when_all_tasks_pass():
    result = create_evolution_result(
        (
            create_task_result("task-1", True),
            create_task_result("task-2", True),
        )
    )

    assert result.passed is True


def test_failed_when_any_task_fails():
    result = create_evolution_result(
        (
            create_task_result("task-1", True),
            create_task_result("task-2", False),
        )
    )

    assert result.passed is False


def test_empty_task_results_are_considered_passed():
    result = create_evolution_result(())

    assert result.passed is True


def test_evolution_result_is_immutable():
    result = create_evolution_result(())

    with pytest.raises(
        AttributeError,
    ):
        result.requested_capability = "changed"