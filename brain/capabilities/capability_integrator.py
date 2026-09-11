from brain.capabilities.capability_registry import (
    CapabilityRegistry,
)
from brain.capabilities.models.capability_descriptor import (
    CapabilityDescriptor,
)


class CapabilityIntegrator:
    def __init__(
        self,
        registry: CapabilityRegistry,
    ):
        if not isinstance(
            registry,
            CapabilityRegistry,
        ):
            raise TypeError(
                "registry must be a CapabilityRegistry"
            )

        self._registry = registry

    def integrate(
        self,
        capability: CapabilityDescriptor,
        verification_passed: bool,
    ) -> None:
        if not isinstance(
            capability,
            CapabilityDescriptor,
        ):
            raise TypeError(
                "capability must be a CapabilityDescriptor"
            )

        if not isinstance(
            verification_passed,
            bool,
        ):
            raise TypeError(
                "verification_passed must be a bool"
            )

        if not verification_passed:
            raise ValueError(
                "cannot integrate an unverified capability"
            )

        self._registry.register(
            capability
        )