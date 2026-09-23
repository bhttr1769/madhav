import subprocess

from brain.evolution.models.evolution_validation_check import (
    EvolutionValidationCheck,
)


class EvolutionSystemRegressionValidator:
    def validate(
        self,
        verification_command: tuple[str, ...],
    ) -> EvolutionValidationCheck:
        if not isinstance(
            verification_command,
            tuple,
        ):
            raise TypeError(
                "verification_command must be a tuple"
            )

        if not verification_command:
            raise ValueError(
                "verification_command must not be empty"
            )

        for argument in verification_command:
            if not isinstance(argument, str):
                raise TypeError(
                    "verification_command must contain "
                    "only strings"
                )

            if not argument:
                raise ValueError(
                    "verification_command arguments "
                    "must not be empty"
                )

        try:
            result = subprocess.run(
                verification_command,
                capture_output=True,
                text=True,
                check=False,
            )
        except OSError as exc:
            return EvolutionValidationCheck(
                name="system_regression_validation",
                passed=False,
                reason=(
                    "system regression verification "
                    f"could not be executed: {exc}"
                ),
            )

        if result.returncode != 0:
            output = (
                result.stderr.strip()
                or result.stdout.strip()
                or "verification command failed without output"
            )

            return EvolutionValidationCheck(
                name="system_regression_validation",
                passed=False,
                reason=(
                    "system regression verification "
                    f"failed: {output}"
                ),
            )

        return EvolutionValidationCheck(
            name="system_regression_validation",
            passed=True,
            reason=(
                "verification command "
                "completed successfully"
            ),
        )