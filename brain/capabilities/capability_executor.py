from brain.capabilities.capability_registry import (
    CapabilityRegistry,
)
from brain.capabilities.entry_point_resolver import (
    EntryPointResolver,
)


class CapabilityExecutor:
    def __init__(
        self,
        registry: CapabilityRegistry,
        resolver: EntryPointResolver | None = None,
    ):
        if not isinstance(
            registry,
            CapabilityRegistry,
        ):
            raise TypeError(
                "registry must be a CapabilityRegistry"
            )

        self._registry = registry
        self._resolver = (
            resolver
            if resolver is not None
            else EntryPointResolver()
        )

    def execute(
        self,
        capability_id: str,
        input_data: object,
    ) -> object:
        if not isinstance(
            capability_id,
            str,
        ):
            raise TypeError(
                "capability_id must be a string"
            )

        if not capability_id.strip():
            raise ValueError(
                "capability_id must not be empty"
            )

        capability = self._registry.get(
            capability_id
        )

        implementation = self._resolver.resolve(
            capability.entry_point
        )

        execute = getattr(
            implementation,
            "execute",
            None,
        )

        if execute is None:
            raise TypeError(
                "capability implementation must "
                "provide an execute method"
            )

        if not callable(execute):
            raise TypeError(
                "capability execute attribute "
                "must be callable"
            )

        return execute(input_data)