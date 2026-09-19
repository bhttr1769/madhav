from brain.capabilities.models.capability_composition import (
    CapabilityComposition,
)
from brain.capabilities.models.capability_descriptor import (
    CapabilityDescriptor,
)


class CapabilityComposer:
    def compose(
        self,
        capability_id: str,
        name: str,
        description: str,
        version: str,
        capabilities: tuple[CapabilityDescriptor, ...],
    ) -> CapabilityComposition:
        if not isinstance(capability_id, str):
            raise TypeError(
                "capability_id must be a string"
            )

        if not capability_id.strip():
            raise ValueError(
                "capability_id must not be empty"
            )

        if not isinstance(name, str):
            raise TypeError(
                "name must be a string"
            )

        if not name.strip():
            raise ValueError(
                "name must not be empty"
            )

        if not isinstance(description, str):
            raise TypeError(
                "description must be a string"
            )

        if not isinstance(version, str):
            raise TypeError(
                "version must be a string"
            )

        if not isinstance(capabilities, tuple):
            raise TypeError(
                "capabilities must be a tuple"
            )

        if not capabilities:
            raise ValueError(
                "capabilities must not be empty"
            )

        for capability in capabilities:
            if not isinstance(
                capability,
                CapabilityDescriptor,
            ):
                raise TypeError(
                    "capabilities must contain only "
                    "CapabilityDescriptor instances"
                )

        return CapabilityComposition(
            id=capability_id,
            name=name,
            description=description,
            version=version,
            capabilities=capabilities,
        )