from brain.capabilities.models.capability_descriptor import (
    CapabilityDescriptor,
)


class CapabilityDiscovery:
    def __init__(
        self,
        providers: tuple[object, ...] = (),
    ):
        if not isinstance(
            providers,
            tuple,
        ):
            raise TypeError(
                "providers must be a tuple"
            )

        self._providers = providers

    def discover(
        self,
        providers: tuple[object, ...] | None = None,
    ) -> tuple[CapabilityDescriptor, ...]:
        if providers is None:
            providers_to_discover = (
                self._providers
            )
        else:
            if not isinstance(
                providers,
                tuple,
            ):
                raise TypeError(
                    "providers must be a tuple"
                )

            providers_to_discover = providers

        capabilities = []

        for provider in providers_to_discover:
            capability = self._discover_provider(
                provider
            )

            if capability is not None:
                capabilities.append(
                    capability
                )

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