import pytest

from brain.engineering.generation.models.code_change import (
    CodeChange,
)
from brain.engineering.loop.models.engineering_loop_iteration import (
    EngineeringLoopIteration,
)
from brain.engineering.loop.models.engineering_loop_result import (
    EngineeringLoopResult,
)
from brain.evolution.evolution_change_validator import (
    EvolutionChangeValidator,
)
from brain.evolution.models.evolution_validation_check import (
    EvolutionValidationCheck,
)


def _passed_engineering_result():
    change = CodeChange(
        path="brain/example.py",
        operation="create",
        content="example",
    )

    iteration = EngineeringLoopIteration(
        iteration=1,
        changes=(change,),
        passed=True,
        summary="Verification passed.",
    )

    return EngineeringLoopResult(
        changes=(change,),
        passed=True,
        iterations=(iteration,),
        termination_reason="verification_passed",
    )


def _failed_engineering_result():
    change = CodeChange(
        path="brain/example.py",
        operation="create",
        content="example",
    )

    iteration = EngineeringLoopIteration(
        iteration=1,
        changes=(change,),
        passed=False,
        summary="Verification failed.",
    )

    return EngineeringLoopResult(
        changes=(change,),
        passed=False,
        iterations=(iteration,),
        termination_reason="max_iterations_reached",
    )


def test_validator_returns_passed_check_for_valid_changes():
    validator = EvolutionChangeValidator()

    changes = (
        CodeChange(
            path="brain/example.py",
            operation="create",
            content="example",
        ),
    )

    result = validator.validate(
        proposed_changes=changes,
        engineering_result=_passed_engineering_result(),
    )

    assert isinstance(
        result,
        EvolutionValidationCheck,
    )

    assert result.name == "change_validation"
    assert result.passed is True


def test_validator_rejects_empty_changes():
    validator = EvolutionChangeValidator()

    result = validator.validate(
        proposed_changes=(),
        engineering_result=_passed_engineering_result(),
    )

    assert result.name == "change_validation"
    assert result.passed is False
    assert result.reason == (
        "evolution produced no proposed changes"
    )


def test_validator_rejects_failed_engineering_result():
    validator = EvolutionChangeValidator()

    changes = (
        CodeChange(
            path="brain/example.py",
            operation="create",
            content="example",
        ),
    )

    result = validator.validate(
        proposed_changes=changes,
        engineering_result=_failed_engineering_result(),
    )

    assert result.name == "change_validation"
    assert result.passed is False
    assert result.reason == (
        "engineering verification did not pass"
    )


def test_validator_rejects_absolute_forward_slash_path():
    validator = EvolutionChangeValidator()

    changes = (
        CodeChange(
            path="/brain/example.py",
            operation="create",
            content="example",
        ),
    )

    result = validator.validate(
        proposed_changes=changes,
        engineering_result=_passed_engineering_result(),
    )

    assert result.passed is False
    assert result.reason == (
        "change path must be relative"
    )


def test_validator_rejects_absolute_backslash_path():
    validator = EvolutionChangeValidator()

    changes = (
        CodeChange(
            path="\\brain\\example.py",
            operation="create",
            content="example",
        ),
    )

    result = validator.validate(
        proposed_changes=changes,
        engineering_result=_passed_engineering_result(),
    )

    assert result.passed is False
    assert result.reason == (
        "change path must be relative"
    )


def test_validator_rejects_parent_traversal():
    validator = EvolutionChangeValidator()

    changes = (
        CodeChange(
            path="brain/../example.py",
            operation="create",
            content="example",
        ),
    )

    result = validator.validate(
        proposed_changes=changes,
        engineering_result=_passed_engineering_result(),
    )

    assert result.passed is False
    assert result.reason == (
        "change path must not contain parent traversal"
    )


def test_validator_rejects_empty_path():
    validator = EvolutionChangeValidator()

    changes = (
        CodeChange(
            path="",
            operation="create",
            content="example",
        ),
    )

    result = validator.validate(
        proposed_changes=changes,
        engineering_result=_passed_engineering_result(),
    )

    assert result.passed is False
    assert result.reason == (
        "change contains an invalid path"
    )


def test_validator_rejects_non_tuple_changes():
    validator = EvolutionChangeValidator()

    with pytest.raises(
        TypeError,
        match="proposed_changes must be a tuple",
    ):
        validator.validate(
            proposed_changes=[],
            engineering_result=_passed_engineering_result(),
        )


def test_validator_rejects_invalid_engineering_result():
    validator = EvolutionChangeValidator()

    changes = (
        CodeChange(
            path="brain/example.py",
            operation="create",
            content="example",
        ),
    )

    with pytest.raises(
        TypeError,
        match="EngineeringLoopResult",
    ):
        validator.validate(
            proposed_changes=changes,
            engineering_result=object(),
        )


def test_validator_rejects_non_code_change_entries():
    validator = EvolutionChangeValidator()

    with pytest.raises(
        TypeError,
        match="CodeChange instances",
    ):
        validator.validate(
            proposed_changes=(object(),),
            engineering_result=_passed_engineering_result(),
        )