from brain.engineering.generation.models.code_change import (
    CodeChange,
)
from brain.engineering.loop.models.engineering_loop_result import (
    EngineeringLoopResult,
)
from brain.capabilities.models.capability_descriptor import (
    CapabilityDescriptor,
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
from brain.evolution.models.evolution_validation_result import (
    EvolutionValidationResult,
)


class EvolutionValidator:
    def __init__(
        self,
        change_validator: EvolutionChangeValidator,
        capability_validator: EvolutionCapabilityValidator,
        system_regression_validator: EvolutionSystemRegressionValidator,
    ):
        if not isinstance(
            change_validator,
            EvolutionChangeValidator,
        ):
            raise TypeError(
                "change_validator must be an EvolutionChangeValidator"
            )

        if not isinstance(
            capability_validator,
            EvolutionCapabilityValidator,
        ):
            raise TypeError(
                "capability_validator must be an EvolutionCapabilityValidator"
            )

        if not isinstance(
            system_regression_validator,
            EvolutionSystemRegressionValidator,
        ):
            raise TypeError(
                "system_regression_validator must be an "
                "EvolutionSystemRegressionValidator"
            )

        self._change_validator = change_validator
        self._capability_validator = capability_validator
        self._system_regression_validator = (
            system_regression_validator
        )

    def validate(
        self,
        proposed_changes: tuple[CodeChange, ...],
        engineering_result: EngineeringLoopResult,
        capabilities: tuple[CapabilityDescriptor, ...],
        requested_capability: str,
        verification_command: tuple[str, ...],
    ) -> EvolutionValidationResult:
        if not isinstance(proposed_changes, tuple):
            raise TypeError(
                "proposed_changes must be a tuple"
            )

        if not isinstance(
            engineering_result,
            EngineeringLoopResult,
        ):
            raise TypeError(
                "engineering_result must be an EngineeringLoopResult"
            )

        if not isinstance(capabilities, tuple):
            raise TypeError(
                "capabilities must be a tuple"
            )

        for capability in capabilities:
            if not isinstance(
                capability,
                CapabilityDescriptor,
            ):
                raise TypeError(
                    "capabilities must contain "
                    "CapabilityDescriptor instances"
                )

        if not isinstance(
            requested_capability,
            str,
        ):
            raise TypeError(
                "requested_capability must be a string"
            )

        if not isinstance(
            verification_command,
            tuple,
        ):
            raise TypeError(
                "verification_command must be a tuple"
            )

        change_check = self._change_validator.validate(
            proposed_changes,
            engineering_result,
        )

        capability_check = self._capability_validator.validate(
            capabilities,
            requested_capability,
        )

        regression_check = (
            self._system_regression_validator.validate(
                verification_command,
            )
        )

        return EvolutionValidationResult(
            checks=(
                change_check,
                capability_check,
                regression_check,
            )
        )