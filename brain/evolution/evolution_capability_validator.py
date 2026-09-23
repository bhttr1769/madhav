from brain.capabilities.models.capability_descriptor import (
    CapabilityDescriptor,
)
from brain.evolution.models.evolution_validation_check import (
    EvolutionValidationCheck,
)


class EvolutionCapabilityValidator:
    def validate(
        self,
        capabilities: tuple[CapabilityDescriptor, ...],
        requested_capability: str,
    ) -> EvolutionValidationCheck:
        if not isinstance(
            capabilities,
            tuple,
        ):
            raise TypeError(
                "capabilities must be a tuple"
            )

        if not isinstance(
            requested_capability,
            str,
        ):
            raise TypeError(
                "requested_capability must be a string"
            )

        requested_capability = (
            requested_capability.strip()
        )

        if not requested_capability:
            raise ValueError(
                "requested_capability must not be empty"
            )

        if not capabilities:
            return EvolutionValidationCheck(
                name="capability_validation",
                passed=False,
                reason=(
                    "no capability descriptor was discovered"
                ),
            )

        if len(capabilities) != 1:
            return EvolutionValidationCheck(
                name="capability_validation",
                passed=False,
                reason=(
                    "exactly one capability descriptor "
                    "must be discovered"
                ),
            )

        capability = capabilities[0]

        if not isinstance(
            capability,
            CapabilityDescriptor,
        ):
            raise TypeError(
                "capabilities must contain "
                "CapabilityDescriptor instances"
            )

        if not isinstance(
            capability.id,
            str,
        ) or not capability.id.strip():
            return EvolutionValidationCheck(
                name="capability_validation",
                passed=False,
                reason=(
                    "capability descriptor must have "
                    "a valid id"
                ),
            )

        if not isinstance(
            capability.name,
            str,
        ) or not capability.name.strip():
            return EvolutionValidationCheck(
                name="capability_validation",
                passed=False,
                reason=(
                    "capability descriptor must have "
                    "a valid name"
                ),
            )

        if not isinstance(
            capability.entry_point,
            str,
        ) or not capability.entry_point.strip():
            return EvolutionValidationCheck(
                name="capability_validation",
                passed=False,
                reason=(
                    "capability descriptor must have "
                    "a valid entry point"
                ),
            )

        if capability.id != requested_capability:
            return EvolutionValidationCheck(
                name="capability_validation",
                passed=False,
                reason=(
                    "discovered capability does not "
                    "match the requested capability"
                ),
            )

        return EvolutionValidationCheck(
            name="capability_validation",
            passed=True,
            reason=(
                "discovered capability descriptor "
                "matches the requested capability"
            ),
        )