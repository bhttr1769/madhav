from brain.engineering.generation.models.code_change import (
    CodeChange,
)

from brain.engineering.testing.models.test_generation_result import (
    TestGenerationResult as GenerationResult,
)


def test_generation_result_contains_test_changes():

    changes = (
        CodeChange(
            path="tests/test_health.py",
            operation="create",
            content="def test_health():\n    assert True\n",
        ),
    )

    result = GenerationResult(
        changes=changes,
    )

    assert result.changes == changes


def test_generation_result_supports_no_test_changes():

    result = GenerationResult(
        changes=(),
    )

    assert result.changes == ()