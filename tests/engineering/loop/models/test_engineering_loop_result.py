from brain.engineering.generation.models.code_change import CodeChange
from brain.engineering.loop.models.engineering_loop_iteration import (
    EngineeringLoopIteration,
)
from brain.engineering.loop.models.engineering_loop_result import (
    EngineeringLoopResult,
)


def test_engineering_loop_result_can_be_constructed():
    changes = (
        CodeChange(
            path="brain/example.py",
            operation="modify",
            content="return value",
        ),
    )

    iteration = EngineeringLoopIteration(
        iteration=1,
        changes=changes,
        passed=True,
        summary="Verification passed.",
    )

    result = EngineeringLoopResult(
        changes=changes,
        passed=True,
        iterations=(iteration,),
        termination_reason="verification_passed",
    )

    assert result.changes == changes
    assert result.passed is True
    assert result.iterations == (iteration,)
    assert result.termination_reason == (
        "verification_passed"
    )