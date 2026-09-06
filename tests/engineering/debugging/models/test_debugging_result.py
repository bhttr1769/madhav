from brain.engineering.debugging.models.debugging_result import (
    DebuggingResult,
)
from brain.engineering.generation.models.code_change import CodeChange


def test_debugging_result_can_be_constructed():
    changes = (
        CodeChange(
            path="brain/example.py",
            operation="modify",
            content="return fixed_value",
        ),
    )

    result = DebuggingResult(
        changes=changes,
        diagnosis="Undefined variable caused the failure.",
    )

    assert result.changes == changes
    assert result.diagnosis == (
        "Undefined variable caused the failure."
    )