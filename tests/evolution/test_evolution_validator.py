from unittest.mock import Mock

import pytest

from brain.capabilities.models.capability_descriptor import (
    CapabilityDescriptor,
)
from brain.engineering.generation.models.code_change import (
    CodeChange,
)
from brain.engineering.loop.models.engineering_loop_result import (
    EngineeringLoopResult,
)
from brain.evolution.evolution_capability_validator import (
    EvolutionCapabilityValidator,
)
from brain.evolution.evolution_change_validator import (
    EvolutionChangeValidator,
)
from brain.evolution.evolution_system_regression_validator import (
    EvolutionSystemRegressionValidator,
)
from brain.evolution.evolution_validator import (
    EvolutionValidator,
)
from brain.evolution.models.evolution_validation_check import (
    EvolutionValidationCheck,
)
from brain.evolution.models.evolution_validation_result import (
    EvolutionValidationResult,
)


class TestEvolutionValidator:

    def _create_validator(
        self,
        change_validator=None,
        capability_validator=None,
        system_regression_validator=None,
    ):
        return EvolutionValidator(
            change_validator=(
                change_validator
                or EvolutionChangeValidator()
            ),
            capability_validator=(
                capability_validator
                or EvolutionCapabilityValidator()
            ),
            system_regression_validator=(
                system_regression_validator
                or EvolutionSystemRegressionValidator()
            ),
        )

    def _create_capability(self):
        return CapabilityDescriptor(
            id="test.capability",
            name="Test Capability",
            description="Test capability",
            version="1.0",
            entry_point="brain.test.TestCapability",
            dependencies=frozenset(),
        )

    def _create_engineering_result(self):
        return EngineeringLoopResult(
            changes=(),
            passed=True,
            iterations=(),
            termination_reason="verification_passed",
        )

    def test_validation_combines_all_checks(self):
        change_validator = Mock(
            spec=EvolutionChangeValidator
        )
        capability_validator = Mock(
            spec=EvolutionCapabilityValidator
        )
        system_regression_validator = Mock(
            spec=EvolutionSystemRegressionValidator
        )

        change_check = EvolutionValidationCheck(
            name="change_validation",
            passed=True,
            reason="changes valid",
        )

        capability_check = EvolutionValidationCheck(
            name="capability_validation",
            passed=True,
            reason="capability valid",
        )

        regression_check = EvolutionValidationCheck(
            name="system_regression_validation",
            passed=True,
            reason="regression validation passed",
        )

        change_validator.validate.return_value = change_check
        capability_validator.validate.return_value = (
            capability_check
        )
        system_regression_validator.validate.return_value = (
            regression_check
        )

        validator = self._create_validator(
            change_validator=change_validator,
            capability_validator=capability_validator,
            system_regression_validator=(
                system_regression_validator
            ),
        )

        result = validator.validate(
            proposed_changes=(),
            engineering_result=self._create_engineering_result(),
            capabilities=(self._create_capability(),),
            requested_capability="test.capability",
            verification_command=("verification",),
        )

        assert isinstance(
            result,
            EvolutionValidationResult,
        )
        assert result.checks == (
            change_check,
            capability_check,
            regression_check,
        )
        assert result.passed is True

        change_validator.validate.assert_called_once()
        capability_validator.validate.assert_called_once()
        system_regression_validator.validate.assert_called_once()

    def test_failed_change_check_fails_evolution_validation(self):
        change_validator = Mock(
            spec=EvolutionChangeValidator
        )
        capability_validator = Mock(
            spec=EvolutionCapabilityValidator
        )
        system_regression_validator = Mock(
            spec=EvolutionSystemRegressionValidator
        )

        change_validator.validate.return_value = (
            EvolutionValidationCheck(
                name="change_validation",
                passed=False,
                reason="invalid change",
            )
        )

        capability_validator.validate.return_value = (
            EvolutionValidationCheck(
                name="capability_validation",
                passed=True,
                reason="capability valid",
            )
        )

        system_regression_validator.validate.return_value = (
            EvolutionValidationCheck(
                name="system_regression_validation",
                passed=True,
                reason="regression validation passed",
            )
        )

        validator = self._create_validator(
            change_validator=change_validator,
            capability_validator=capability_validator,
            system_regression_validator=(
                system_regression_validator
            ),
        )

        result = validator.validate(
            proposed_changes=(),
            engineering_result=self._create_engineering_result(),
            capabilities=(self._create_capability(),),
            requested_capability="test.capability",
            verification_command=("verification",),
        )

        assert result.passed is False
        assert result.checks[0].passed is False

    def test_failed_capability_check_fails_evolution_validation(self):
        change_validator = Mock(
            spec=EvolutionChangeValidator
        )
        capability_validator = Mock(
            spec=EvolutionCapabilityValidator
        )
        system_regression_validator = Mock(
            spec=EvolutionSystemRegressionValidator
        )

        change_validator.validate.return_value = (
            EvolutionValidationCheck(
                name="change_validation",
                passed=True,
                reason="changes valid",
            )
        )

        capability_validator.validate.return_value = (
            EvolutionValidationCheck(
                name="capability_validation",
                passed=False,
                reason="capability mismatch",
            )
        )

        system_regression_validator.validate.return_value = (
            EvolutionValidationCheck(
                name="system_regression_validation",
                passed=True,
                reason="regression validation passed",
            )
        )

        validator = self._create_validator(
            change_validator=change_validator,
            capability_validator=capability_validator,
            system_regression_validator=(
                system_regression_validator
            ),
        )

        result = validator.validate(
            proposed_changes=(),
            engineering_result=self._create_engineering_result(),
            capabilities=(self._create_capability(),),
            requested_capability="test.capability",
            verification_command=("verification",),
        )

        assert result.passed is False
        assert result.checks[1].passed is False

    def test_failed_regression_check_fails_evolution_validation(self):
        change_validator = Mock(
            spec=EvolutionChangeValidator
        )
        capability_validator = Mock(
            spec=EvolutionCapabilityValidator
        )
        system_regression_validator = Mock(
            spec=EvolutionSystemRegressionValidator
        )

        change_validator.validate.return_value = (
            EvolutionValidationCheck(
                name="change_validation",
                passed=True,
                reason="changes valid",
            )
        )

        capability_validator.validate.return_value = (
            EvolutionValidationCheck(
                name="capability_validation",
                passed=True,
                reason="capability valid",
            )
        )

        system_regression_validator.validate.return_value = (
            EvolutionValidationCheck(
                name="system_regression_validation",
                passed=False,
                reason="regression detected",
            )
        )

        validator = self._create_validator(
            change_validator=change_validator,
            capability_validator=capability_validator,
            system_regression_validator=(
                system_regression_validator
            ),
        )

        result = validator.validate(
            proposed_changes=(),
            engineering_result=self._create_engineering_result(),
            capabilities=(self._create_capability(),),
            requested_capability="test.capability",
            verification_command=("verification",),
        )

        assert result.passed is False
        assert result.checks[2].passed is False

    def test_constructor_rejects_invalid_change_validator(self):
        with pytest.raises(TypeError):
            EvolutionValidator(
                change_validator=object(),
                capability_validator=(
                    EvolutionCapabilityValidator()
                ),
                system_regression_validator=(
                    EvolutionSystemRegressionValidator()
                ),
            )

    def test_constructor_rejects_invalid_capability_validator(self):
        with pytest.raises(TypeError):
            EvolutionValidator(
                change_validator=EvolutionChangeValidator(),
                capability_validator=object(),
                system_regression_validator=(
                    EvolutionSystemRegressionValidator()
                ),
            )

    def test_constructor_rejects_invalid_regression_validator(self):
        with pytest.raises(TypeError):
            EvolutionValidator(
                change_validator=EvolutionChangeValidator(),
                capability_validator=(
                    EvolutionCapabilityValidator()
                ),
                system_regression_validator=object(),
            )

    def test_invalid_proposed_changes_are_rejected(self):
        validator = self._create_validator()

        with pytest.raises(TypeError):
            validator.validate(
                proposed_changes=[],
                engineering_result=(
                    self._create_engineering_result()
                ),
                capabilities=(self._create_capability(),),
                requested_capability="test.capability",
                verification_command=("verification",),
            )

    def test_invalid_engineering_result_is_rejected(self):
        validator = self._create_validator()

        with pytest.raises(TypeError):
            validator.validate(
                proposed_changes=(),
                engineering_result=object(),
                capabilities=(self._create_capability(),),
                requested_capability="test.capability",
                verification_command=("verification",),
            )

    def test_invalid_capabilities_container_is_rejected(self):
        validator = self._create_validator()

        with pytest.raises(TypeError):
            validator.validate(
                proposed_changes=(),
                engineering_result=(
                    self._create_engineering_result()
                ),
                capabilities=[],
                requested_capability="test.capability",
                verification_command=("verification",),
            )

    def test_invalid_capability_item_is_rejected(self):
        validator = self._create_validator()

        with pytest.raises(TypeError):
            validator.validate(
                proposed_changes=(),
                engineering_result=(
                    self._create_engineering_result()
                ),
                capabilities=(object(),),
                requested_capability="test.capability",
                verification_command=("verification",),
            )

    def test_invalid_requested_capability_is_rejected(self):
        validator = self._create_validator()

        with pytest.raises(TypeError):
            validator.validate(
                proposed_changes=(),
                engineering_result=(
                    self._create_engineering_result()
                ),
                capabilities=(self._create_capability(),),
                requested_capability=123,
                verification_command=("verification",),
            )

    def test_invalid_verification_command_is_rejected(self):
        validator = self._create_validator()

        with pytest.raises(TypeError):
            validator.validate(
                proposed_changes=(),
                engineering_result=(
                    self._create_engineering_result()
                ),
                capabilities=(self._create_capability(),),
                requested_capability="test.capability",
                verification_command=["verification"],
            )