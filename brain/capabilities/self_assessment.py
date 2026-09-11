from brain.capabilities.capability_registry import (
    CapabilityRegistry,
)
from brain.capabilities.models.capability_assessment import (
    CapabilityAssessment,
)


class SelfAssessment:
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

    def assess(
        self,
        requested_capability: str,
    ) -> CapabilityAssessment:
        if not isinstance(
            requested_capability,
            str,
        ):
            raise TypeError(
                "requested_capability must be a string"
            )

        if not requested_capability.strip():
            raise ValueError(
                "requested_capability must not be empty"
            )

        if self._registry.has(
            requested_capability
        ):
            return CapabilityAssessment(
                requested_capability=(
                    requested_capability
                ),
                available=True,
                status="available",
                matched_capabilities=frozenset(
                    {requested_capability}
                ),
                missing_capabilities=frozenset(),
                rationale=(
                    "The requested capability "
                    "is registered."
                ),
            )

        return CapabilityAssessment(
            requested_capability=requested_capability,
            available=False,
            status="unavailable",
            matched_capabilities=frozenset(),
            missing_capabilities=frozenset(
                {requested_capability}
            ),
            rationale=(
                "The requested capability "
                "is not registered."
            ),
        )