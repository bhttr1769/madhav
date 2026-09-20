import pytest

from brain.engineering.loop.models.engineering_loop_result import (
    EngineeringLoopResult,
)
from brain.evolution.evolution_failure_policy import (
    EvolutionFailurePolicy,
)
from brain.evolution.models.evolution_task_result import (
    EvolutionTaskResult,
)


def create_task_result(
    passed: bool,
) -> EvolutionTaskResult:
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
        task_id="task-1",
        task_description="Test task",
        proposed_changes=(),
        engineering_result=engineering_result,
    )


def test_should_not_stop_when_task_succeeds():
    policy = EvolutionFailurePolicy()

    result = policy.should_stop(
        create_task_result(True),
    )

    assert result is False


def test_should_stop_when_task_fails():
    policy = EvolutionFailurePolicy()

    result = policy.should_stop(
        create_task_result(False),
    )

    assert result is True


def test_rejects_invalid_task_result():
    policy = EvolutionFailurePolicy()

    with pytest.raises(
        TypeError,
        match="EvolutionTaskResult",
    ):
        policy.should_stop("invalid")