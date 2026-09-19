from brain.capabilities.models.capability_descriptor import (
    CapabilityDescriptor,
)


class CapabilityMatcher:
    def match(
        self,
        required_capabilities: frozenset[str],
        available_capabilities: tuple[
            CapabilityDescriptor,
            ...,
        ],
    ) -> frozenset[str]:
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

        return frozenset(
            capability_id
            for capability_id in required_capabilities
            if capability_id in available_ids
        )