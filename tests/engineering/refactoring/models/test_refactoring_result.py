from brain.engineering.generation.models.code_change import CodeChange
from brain.engineering.refactoring.models.refactoring_result import (
    RefactoringResult,
)


def test_refactoring_result_can_be_constructed():
    changes = (
        CodeChange(
            path="brain/example.py",
            operation="modify",
            content="return value",
        ),
    )

    result = RefactoringResult(
        changes=changes,
        rationale=(
            "The implementation was simplified "
            "without changing behavior."
        ),
    )

    assert result.changes == changes
    assert result.rationale == (
        "The implementation was simplified "
        "without changing behavior."
    )