from brain.capabilities.models.capability_descriptor import CapabilityDescriptor
from brain.evolution.capability_dependency_resolver import CapabilityDependencyResolver


class CapabilityFeasibilityChecker:
    def __init__(
        self,
        dependency_resolver: CapabilityDependencyResolver | None = None,
    ):
        self._dependency_resolver = (
            dependency_resolver
            if dependency_resolver is not None
            else CapabilityDependencyResolver()
        )

    def check(
        self,
        required_capabilities: frozenset[str],
        available_capabilities: tuple[CapabilityDescriptor, ...],
    ) -> frozenset[str]:
        if not isinstance(required_capabilities, frozenset):
            raise TypeError(
                "required_capabilities must be a frozenset"
            )

        for capability_id in required_capabilities:
            if not isinstance(capability_id, str):
                raise TypeError(
                    "required_capabilities must contain only strings"
                )

        if not isinstance(available_capabilities, tuple):
            raise TypeError(
                "available_capabilities must be a tuple"
            )

        for capability in available_capabilities:
            if not isinstance(capability, CapabilityDescriptor):
                raise TypeError(
                    "available_capabilities must contain only "
                    "CapabilityDescriptor instances"
                )

        # Preserve the existing resolver's dependency-cycle semantics.
        self._dependency_resolver.resolve(
            required_capabilities=required_capabilities,
            available_capabilities=available_capabilities,
        )

        capabilities_by_id = {
            capability.id: capability
            for capability in available_capabilities
        }

        required_with_dependencies = set(required_capabilities)
        pending = list(required_capabilities)

        while pending:
            capability_id = pending.pop()

            capability = capabilities_by_id.get(capability_id)

            if capability is None:
                continue

            for dependency in capability.dependencies:
                if dependency not in required_with_dependencies:
                    required_with_dependencies.add(dependency)
                    pending.append(dependency)

        available_ids = frozenset(capabilities_by_id)

        return frozenset(
            capability_id
            for capability_id in required_with_dependencies
            if capability_id not in available_ids
        )