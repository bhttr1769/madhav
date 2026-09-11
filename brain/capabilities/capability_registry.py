from brain.capabilities.models.capability_descriptor import (
    CapabilityDescriptor,
)


class CapabilityRegistry:
    def __init__(
        self,
        capabilities: tuple[CapabilityDescriptor, ...] = (),
    ):
        self._capabilities = {}

        for capability in capabilities:
            self.register(capability)

    def register(
        self,
        capability: CapabilityDescriptor,
    ) -> None:
        if not isinstance(
            capability,
            CapabilityDescriptor,
        ):
            raise TypeError(
                "capability must be a CapabilityDescriptor"
            )

        if capability.id in self._capabilities:
            raise ValueError(
                f"capability already registered: "
                f"{capability.id}"
            )

        self._capabilities[capability.id] = capability

    def get(
        self,
        capability_id: str,
    ) -> CapabilityDescriptor:
        try:
            return self._capabilities[capability_id]
        except KeyError as exc:
            raise KeyError(
                f"capability not found: {capability_id}"
            ) from exc

    def has(
        self,
        capability_id: str,
    ) -> bool:
        return capability_id in self._capabilities

    def all(
        self,
    ) -> tuple[CapabilityDescriptor, ...]:
        return tuple(
            self._capabilities.values()
        )

    def unregister(
        self,
        capability_id: str,
    ) -> None:
        if capability_id not in self._capabilities:
            raise KeyError(
                f"capability not found: {capability_id}"
            )

        del self._capabilities[capability_id]