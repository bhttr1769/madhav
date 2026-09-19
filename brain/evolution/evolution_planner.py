from brain.capabilities.models.capability_assessment import (
    CapabilityAssessment,
)
from brain.evolution.capability_dependency_resolver import (
    CapabilityDependencyResolver,
)
from brain.evolution.evolution_task_generator import (
    EvolutionTaskGenerator,
)
from brain.evolution.evolution_validation_strategy import (
    EvolutionValidationStrategy,
)
from brain.evolution.models.evolution_plan import (
    EvolutionPlan,
)
from brain.evolution.models.evolution_planning_context import (
    EvolutionPlanningContext,
)
from brain.evolution.models.evolution_request import (
    EvolutionRequest,
)


class EvolutionPlanner:
    def __init__(
        self,
        dependency_resolver=None,
        task_generator=None,
        validation_strategy=None,
    ):
        self._dependency_resolver = (
            dependency_resolver
            if dependency_resolver is not None
            else CapabilityDependencyResolver()
        )

        self._task_generator = (
            task_generator
            if task_generator is not None
            else EvolutionTaskGenerator()
        )

        self._validation_strategy = (
            validation_strategy
            if validation_strategy is not None
            else EvolutionValidationStrategy()
        )

    def plan(
        self,
        request: EvolutionRequest,
        assessment: CapabilityAssessment,
        available_capabilities=(),
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

        if not isinstance(
            available_capabilities,
            tuple,
        ):
            raise TypeError(
                "available_capabilities must be a tuple"
            )

        context = EvolutionPlanningContext(
            request=request,
            assessment=assessment,
            available_capabilities=(
                available_capabilities
            ),
        )

        if context.assessment.available:
            return EvolutionPlan(
                requested_capability=(
                    context.request.requested_capability
                ),
                objective=context.request.objective,
                current_status="already_available",
                reusable_capabilities=(
                    context.assessment.matched_capabilities
                ),
                required_capabilities=frozenset(),
                tasks=(),
                risks=frozenset(),
                validation_strategy=(
                    self._validation_strategy.create(
                        ()
                    )
                ),
            )

        required_capabilities = frozenset(
            {
                context.request.requested_capability,
            }
        )

        resolved_capabilities = (
            self._dependency_resolver.resolve(
                required_capabilities=(
                    required_capabilities
                ),
                available_capabilities=(
                    context.available_capabilities
                ),
            )
        )

        reusable_capabilities = (
            resolved_capabilities
            & frozenset(
                capability.id
                for capability
                in context.available_capabilities
            )
        )

        tasks = self._task_generator.generate(
            required_capabilities=required_capabilities,
            available_capabilities=(
                context.available_capabilities
            ),
        )

        validation_strategy = (
            self._validation_strategy.create(
                tasks
            )
        )

        missing_capabilities = (
            required_capabilities
            - reusable_capabilities
        )

        risks = (
            frozenset(
                {
                    "implementation may fail verification",
                }
            )
            if missing_capabilities
            else frozenset()
        )

        return EvolutionPlan(
            requested_capability=(
                context.request.requested_capability
            ),
            objective=context.request.objective,
            current_status="missing",
            reusable_capabilities=(
                reusable_capabilities
            ),
            required_capabilities=(
                missing_capabilities
            ),
            tasks=tasks,
            risks=risks,
            validation_strategy=(
                validation_strategy
            ),
        )