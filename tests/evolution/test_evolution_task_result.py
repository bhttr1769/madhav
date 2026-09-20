import pytest

from brain.engineering.generation.models.code_change import (
    CodeChange,
)
from brain.engineering.loop.models.engineering_loop_result import (
    EngineeringLoopResult,
)
from brain.evolution.models.evolution_task_result import (
    EvolutionTaskResult,
)


def create_engineering_result():
    return EngineeringLoopResult(
        changes=(),
        passed=True,
        iterations=(),
        termination_reason="verification_passed",
    )


def test_creates_evolution_task_result():
    engineering_result = create_engineering_result()

    result = EvolutionTaskResult(
        task_id="task-1",
        task_description="Implement repository analysis.",
        proposed_changes=(),
        engineering_result=engineering_result,
    )

    assert result.task_id == "task-1"
    assert result.task_description == (
        "Implement repository analysis."
    )
    assert result.proposed_changes == ()
    assert result.engineering_result == (
        engineering_result
    )


def test_evolution_task_result_is_immutable():
    result = EvolutionTaskResult(
        task_id="task-1",
        task_description="Implement repository analysis.",
        proposed_changes=(),
        engineering_result=create_engineering_result(),
    )

    with pytest.raises(
        AttributeError,
    ):
        result.task_id = "task-2"