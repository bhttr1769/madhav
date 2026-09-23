from unittest.mock import patch

import pytest

from brain.evolution.evolution_system_regression_validator import (
    EvolutionSystemRegressionValidator,
)
from brain.evolution.models.evolution_validation_check import (
    EvolutionValidationCheck,
)


class TestEvolutionSystemRegressionValidator:

    def test_successful_command_passes(self):
        validator = EvolutionSystemRegressionValidator()

        completed = type(
            "CompletedProcess",
            (),
            {
                "returncode": 0,
                "stdout": "all tests passed",
                "stderr": "",
            },
        )()

        with patch(
            "brain.evolution.evolution_system_regression_validator.subprocess.run",
            return_value=completed,
        ) as run:
            result = validator.validate(
                ("python", "-m", "pytest")
            )

        assert isinstance(result, EvolutionValidationCheck)
        assert result.name == "system_regression_validation"
        assert result.passed is True
        assert "completed successfully" in result.reason
        run.assert_called_once_with(
            ("python", "-m", "pytest"),
            capture_output=True,
            text=True,
            check=False,
        )

    def test_failed_command_fails(self):
        validator = EvolutionSystemRegressionValidator()

        completed = type(
            "CompletedProcess",
            (),
            {
                "returncode": 1,
                "stdout": "",
                "stderr": "1 failed",
            },
        )()

        with patch(
            "brain.evolution.evolution_system_regression_validator.subprocess.run",
            return_value=completed,
        ):
            result = validator.validate(
                ("python", "-m", "pytest")
            )

        assert result.passed is False
        assert "1 failed" in result.reason

    def test_stdout_is_used_when_stderr_is_empty(self):
        validator = EvolutionSystemRegressionValidator()

        completed = type(
            "CompletedProcess",
            (),
            {
                "returncode": 1,
                "stdout": "regression detected",
                "stderr": "",
            },
        )()

        with patch(
            "brain.evolution.evolution_system_regression_validator.subprocess.run",
            return_value=completed,
        ):
            result = validator.validate(
                ("verification",)
            )

        assert result.passed is False
        assert "regression detected" in result.reason

    def test_failure_without_output_has_default_reason(self):
        validator = EvolutionSystemRegressionValidator()

        completed = type(
            "CompletedProcess",
            (),
            {
                "returncode": 1,
                "stdout": "",
                "stderr": "",
            },
        )()

        with patch(
            "brain.evolution.evolution_system_regression_validator.subprocess.run",
            return_value=completed,
        ):
            result = validator.validate(
                ("verification",)
            )

        assert result.passed is False
        assert (
            "verification command failed without output"
            in result.reason
        )

    def test_execution_error_fails_validation(self):
        validator = EvolutionSystemRegressionValidator()

        with patch(
            "brain.evolution.evolution_system_regression_validator.subprocess.run",
            side_effect=OSError("command not found"),
        ):
            result = validator.validate(
                ("verification",)
            )

        assert result.passed is False
        assert "command not found" in result.reason

    def test_empty_command_is_rejected(self):
        validator = EvolutionSystemRegressionValidator()

        with pytest.raises(ValueError):
            validator.validate(())

    def test_non_tuple_command_is_rejected(self):
        validator = EvolutionSystemRegressionValidator()

        with pytest.raises(TypeError):
            validator.validate(
                ["python", "-m", "pytest"]
            )

    def test_command_arguments_must_be_strings(self):
        validator = EvolutionSystemRegressionValidator()

        with pytest.raises(TypeError):
            validator.validate(
                ("python", 123)
            )

    def test_empty_command_argument_is_rejected(self):
        validator = EvolutionSystemRegressionValidator()

        with pytest.raises(ValueError):
            validator.validate(
                ("python", "")
            )