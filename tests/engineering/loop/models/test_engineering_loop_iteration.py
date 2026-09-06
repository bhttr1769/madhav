from brain.engineering.generation.models.code_change import CodeChange
from brain.engineering.loop.models.engineering_loop_iteration import (
    EngineeringLoopIteration,
)


def test_engineering_loop_iteration_can_be_constructed():
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
        passed=False,
        summary="Verification failed.",
    )

    assert iteration.iteration == 1
    assert iteration.changes == changes
    assert iteration.passed is False
    assert iteration.summary == "Verification failed."