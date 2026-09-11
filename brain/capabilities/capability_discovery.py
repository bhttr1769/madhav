from brain.capabilities.models.capability_descriptor import (
    CapabilityDescriptor,
)


class CapabilityDiscovery:
    def __init__(
        self,
        providers: tuple[object, ...] = (),
    ):
        self._providers = providers

    def discover(
        self,
    ) -> tuple[CapabilityDescriptor, ...]:
        capabilities = []

        for provider in self._providers:
            capability = self._discover_provider(
                provider
            )

            if capability is not None:
                capabilities.append(capability)

        return tuple(capabilities)

    @staticmethod
    def _discover_provider(
        provider: object,
    ) -> CapabilityDescriptor | None:
        discover = getattr(
            provider,
            "capability_descriptor",
            None,
        )

        if discover is None:
            return None

        if not callable(discover):
            raise TypeError(
                "capability_descriptor must be callable"
            )

        capability = discover()

        if not isinstance(
            capability,
            CapabilityDescriptor,
        ):
            raise TypeError(
                "capability_descriptor must return "
                "a CapabilityDescriptor"
            )

        return capability
