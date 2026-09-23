from brain.engineering.generation.models.code_change import (
    CodeChange,
)
from brain.engineering.loop.models.engineering_loop_result import (
    EngineeringLoopResult,
)
from brain.evolution.models.evolution_validation_check import (
    EvolutionValidationCheck,
)


class EvolutionChangeValidator:
    def validate(
        self,
        proposed_changes: tuple[CodeChange, ...],
        engineering_result: EngineeringLoopResult,
    ) -> EvolutionValidationCheck:
        if not isinstance(
            proposed_changes,
            tuple,
        ):
            raise TypeError(
                "proposed_changes must be a tuple"
            )

        if not isinstance(
            engineering_result,
            EngineeringLoopResult,
        ):
            raise TypeError(
                "engineering_result must be an "
                "EngineeringLoopResult"
            )

        if not proposed_changes:
            return EvolutionValidationCheck(
                name="change_validation",
                passed=False,
                reason=(
                    "evolution produced no proposed changes"
                ),
            )

        for change in proposed_changes:
            if not isinstance(
                change,
                CodeChange,
            ):
                raise TypeError(
                    "proposed_changes must contain "
                    "CodeChange instances"
                )

            if not isinstance(
                change.path,
                str,
            ) or not change.path.strip():
                return EvolutionValidationCheck(
                    name="change_validation",
                    passed=False,
                    reason=(
                        "change contains an invalid path"
                    ),
                )

            if change.path.startswith(
                "/"
            ) or change.path.startswith(
                "\\"
            ):
                return EvolutionValidationCheck(
                    name="change_validation",
                    passed=False,
                    reason=(
                        "change path must be relative"
                    ),
                )

            if ".." in change.path.replace(
                "\\",
                "/",
            ).split("/"):
                return EvolutionValidationCheck(
                    name="change_validation",
                    passed=False,
                    reason=(
                        "change path must not contain "
                        "parent traversal"
                    ),
                )

        if not engineering_result.passed:
            return EvolutionValidationCheck(
                name="change_validation",
                passed=False,
                reason=(
                    "engineering verification did not pass"
                ),
            )

        return EvolutionValidationCheck(
            name="change_validation",
            passed=True,
            reason=(
                "proposed changes passed structural "
                "and engineering validation"
            ),
        )