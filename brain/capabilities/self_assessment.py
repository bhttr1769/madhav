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
        requested_capability: str | frozenset[str],
    ) -> CapabilityAssessment:
        if isinstance(
            requested_capability,
            str,
        ):
            if not requested_capability.strip():
                raise ValueError(
                    "requested_capability must not be empty"
                )

            required_capabilities = frozenset(
                {requested_capability}
            )

        elif isinstance(
            requested_capability,
            frozenset,
        ):
            if not requested_capability:
                raise ValueError(
                    "requested_capability must not be empty"
                )

            for capability_id in requested_capability:
                if not isinstance(
                    capability_id,
                    str,
                ):
                    raise TypeError(
                        "requested_capability must contain "
                        "only strings"
                    )

                if not capability_id.strip():
                    raise ValueError(
                        "requested_capability must not contain "
                        "empty capability identifiers"
                    )

            required_capabilities = requested_capability

        else:
            raise TypeError(
                "requested_capability must be a string "
                "or frozenset"
            )

        matched_capabilities = frozenset(
            capability_id
            for capability_id in required_capabilities
            if self._registry.has(capability_id)
        )

        missing_capabilities = (
            required_capabilities
            - matched_capabilities
        )

        available = not missing_capabilities

        if available:
            status = "available"

            if isinstance(requested_capability, str):
                rationale = (
                    "The requested capability "
                    "is registered."
                )
            else:
                rationale = (
                    "All requested capabilities "
                    "are registered."
                )

        else:
            status = "unavailable"
  
            if isinstance(requested_capability, str):
                 rationale = (
                    "The requested capability "
                    "is not registered."
                )  
            else:
                rationale = (
                    "One or more requested capabilities "
                    "are not registered."
                )

        return CapabilityAssessment(
            requested_capability=requested_capability,
            available=available,
            status=status,
            matched_capabilities=matched_capabilities,
            missing_capabilities=missing_capabilities,
            rationale=rationale,
        )