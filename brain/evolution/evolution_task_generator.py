from brain.capabilities.models.capability_descriptor import (
    CapabilityDescriptor,
)


class EvolutionTaskGenerator:
    def generate(
        self,
        required_capabilities: frozenset[str],
        available_capabilities: tuple[
            CapabilityDescriptor,
            ...,
        ],
    ) -> tuple[str, ...]:
        if not isinstance(
            required_capabilities,
            frozenset,
        ):
            raise TypeError(
                "required_capabilities must be a frozenset"
            )

        if not isinstance(
            available_capabilities,
            tuple,
        ):
            raise TypeError(
                "available_capabilities must be a tuple"
            )

        for capability in available_capabilities:
            if not isinstance(
                capability,
                CapabilityDescriptor,
            ):
                raise TypeError(
                    "available_capabilities must contain "
                    "only CapabilityDescriptor instances"
                )

        available_ids = frozenset(
            capability.id
            for capability in available_capabilities
        )

        missing_capabilities = (
            required_capabilities
            - available_ids
        )

        tasks = []

        for capability_id in sorted(
            missing_capabilities
        ):
            tasks.append(
                f"implement capability: {capability_id}"
            )

        return tuple(tasks)