import pytest

from brain.evolution.models.evolution_validation_check import (
    EvolutionValidationCheck,
)
from brain.evolution.models.evolution_validation_result import (
    EvolutionValidationResult,
)


def test_evolution_validation_check_is_immutable():
    check = EvolutionValidationCheck(
        name="change_validation",
        passed=True,
        reason="Changes passed validation.",
    )

    with pytest.raises(
        AttributeError,
    ):
        check.passed = False


def test_evolution_validation_result_preserves_checks():
    first = EvolutionValidationCheck(
        name="change_validation",
        passed=True,
        reason="Changes passed validation.",
    )

    second = EvolutionValidationCheck(
        name="capability_validation",
        passed=True,
        reason="Capability passed validation.",
    )

    result = EvolutionValidationResult(
        checks=(first, second),
    )

    assert result.checks == (
        first,
        second,
    )


def test_evolution_validation_result_passes_when_all_checks_pass():
    result = EvolutionValidationResult(
        checks=(
            EvolutionValidationCheck(
                name="change_validation",
                passed=True,
                reason="Changes passed validation.",
            ),
            EvolutionValidationCheck(
                name="capability_validation",
                passed=True,
                reason="Capability passed validation.",
            ),
            EvolutionValidationCheck(
                name="system_validation",
                passed=True,
                reason="System passed validation.",
            ),
            EvolutionValidationCheck(
                name="evolution_validation",
                passed=True,
                reason="Evolution passed validation.",
            ),
        ),
    )

    assert result.passed is True


def test_evolution_validation_result_fails_when_any_check_fails():
    result = EvolutionValidationResult(
        checks=(
            EvolutionValidationCheck(
                name="change_validation",
                passed=True,
                reason="Changes passed validation.",
            ),
            EvolutionValidationCheck(
                name="capability_validation",
                passed=False,
                reason="Capability validation failed.",
            ),
            EvolutionValidationCheck(
                name="system_validation",
                passed=True,
                reason="System passed validation.",
            ),
        ),
    )

    assert result.passed is False


def test_evolution_validation_result_is_immutable():
    result = EvolutionValidationResult(
        checks=(),
    )

    with pytest.raises(
        AttributeError,
    ):
        result.checks = ()


def test_evolution_validation_check_requires_expected_types():
    check = EvolutionValidationCheck(
        name="change_validation",
        passed=True,
        reason="valid",
    )

    assert isinstance(
        check.name,
        str,
    )

    assert isinstance(
        check.passed,
        bool,
    )

    assert isinstance(
        check.reason,
        str,
    )