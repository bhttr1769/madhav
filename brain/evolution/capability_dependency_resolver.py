from brain.capabilities.models.capability_descriptor import (
    CapabilityDescriptor,
)


class CapabilityDependencyResolver:
    def resolve(
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

        capabilities_by_id = {
            capability.id: capability
            for capability in available_capabilities
        }

        resolved = set()
        visiting = set()

        for capability_id in required_capabilities:
            self._resolve(
                capability_id=capability_id,
                capabilities_by_id=capabilities_by_id,
                resolved=resolved,
                visiting=visiting,
            )

        return frozenset(resolved)

    def _resolve(
        self,
        capability_id: str,
        capabilities_by_id: dict[
            str,
            CapabilityDescriptor,
        ],
        resolved: set[str],
        visiting: set[str],
    ) -> None:
        if capability_id in resolved:
            return

        if capability_id in visiting:
            raise ValueError(
                "cyclic capability dependency detected: "
                f"{capability_id}"
            )

        capability = capabilities_by_id.get(
            capability_id
        )

        if capability is None:
            return

        visiting.add(capability_id)

        for dependency in capability.dependencies:
            self._resolve(
                capability_id=dependency,
                capabilities_by_id=capabilities_by_id,
                resolved=resolved,
                visiting=visiting,
            )

        visiting.remove(capability_id)
        resolved.add(capability_id)