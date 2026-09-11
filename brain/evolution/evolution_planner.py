from brain.capabilities.models.capability_assessment import (
    CapabilityAssessment,
)
from brain.evolution.models.evolution_plan import (
    EvolutionPlan,
)
from brain.evolution.models.evolution_request import (
    EvolutionRequest,
)


class EvolutionPlanner:
    def plan(
        self,
        request: EvolutionRequest,
        assessment: CapabilityAssessment,
    ) -> EvolutionPlan:
        if not isinstance(
            request,
            EvolutionRequest,
        ):
            raise TypeError(
                "request must be an EvolutionRequest"
            )

        if not isinstance(
            assessment,
            CapabilityAssessment,
        ):
            raise TypeError(
                "assessment must be a CapabilityAssessment"
            )

        if (
            request.requested_capability
            != assessment.requested_capability
        ):
            raise ValueError(
                "request and assessment refer to "
                "different capabilities"
            )

        if assessment.available:
            return EvolutionPlan(
                requested_capability=(
                    request.requested_capability
                ),
                objective=request.objective,
                current_status="already_available",
                reusable_capabilities=(
                    assessment.matched_capabilities
                ),
                required_capabilities=frozenset(),
                tasks=(),
                risks=frozenset(),
                validation_strategy=(
                    "verify existing capability",
                ),
            )

        return EvolutionPlan(
            requested_capability=(
                request.requested_capability
            ),
            objective=request.objective,
            current_status="missing",
            reusable_capabilities=(
                assessment.matched_capabilities
            ),
            required_capabilities=frozenset(
                {request.requested_capability}
            ),
            tasks=(
                "analyze capability requirements",
                "design capability architecture",
                "implement capability",
                "generate tests",
                "review implementation",
                "verify implementation",
            ),
            risks=frozenset(
                {"implementation may fail verification"}
            ),
            validation_strategy=(
                "run generated tests",
                "run existing engineering tests",
                "verify capability integration",
            ),
        )