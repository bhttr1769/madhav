from brain.engineering.generation.models.code_change import CodeChange
from brain.engineering.improvement.models.engineering_improvement_result import (
    EngineeringImprovementResult,
)


def test_engineering_improvement_result_can_be_constructed():
    changes = (
        CodeChange(
            path="brain/example.py",
            operation="modify",
            content="return value",
        ),
    )

    rationale = (
        "The implementation can be simplified.",
        "The resulting structure is easier to maintain.",
    )

    result = EngineeringImprovementResult(
        changes=changes,
        rationale=rationale,
    )

    assert result.changes == changes
    assert result.rationale == rationale