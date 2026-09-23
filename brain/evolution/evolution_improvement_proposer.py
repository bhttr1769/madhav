from brain.evolution.models.evolution_improvement_category import (
    EvolutionImprovementCategory,
)

from brain.evolution.models.evolution_improvement_observation import (
    EvolutionImprovementObservation,
)

from brain.evolution.models.evolution_improvement_proposal import (
    EvolutionImprovementProposal,
)


class EvolutionImprovementProposer:
    """
    Converts an improvement observation into a
    deterministic, structured improvement proposal.

    This component does not execute improvements,
    modify source code, or make autonomous decisions.
    """

    _TARGET_COMPONENTS = {
        EvolutionImprovementCategory.REQUIREMENT_UNDERSTANDING: (
            "requirement_understanding"
        ),
        EvolutionImprovementCategory.TASK_DECOMPOSITION: (
            "task_decomposer"
        ),
        EvolutionImprovementCategory.SYSTEM_DESIGN: (
            "system_designer"
        ),
        EvolutionImprovementCategory.ENGINEERING_PLANNING: (
            "planner"
        ),
        EvolutionImprovementCategory.CODE_GENERATION: (
            "engineering_generation"
        ),
        EvolutionImprovementCategory.TEST_GENERATION: (
            "test_generator"
        ),
        EvolutionImprovementCategory.VERIFICATION: (
            "evolution_validator"
        ),
        EvolutionImprovementCategory.DEBUGGING: (
            "engineering_loop"
        ),
        EvolutionImprovementCategory.REFACTORING: (
            "engineering_loop"
        ),
        EvolutionImprovementCategory.CAPABILITY_DISCOVERY: (
            "capability_discovery"
        ),
        EvolutionImprovementCategory.CAPABILITY_INTEGRATION: (
            "capability_integrator"
        ),
        EvolutionImprovementCategory.DEPENDENCY_MANAGEMENT: (
            "dependency_management"
        ),
        EvolutionImprovementCategory.SAFETY: (
            "evolution_safety_policy"
        ),
        EvolutionImprovementCategory.RECOVERY: (
            "evolution_recovery"
        ),
        EvolutionImprovementCategory.ORCHESTRATION: (
            "evolution_executor"
        ),
    }

    def propose(
        self,
        observation: EvolutionImprovementObservation,
    ) -> EvolutionImprovementProposal:
        if not isinstance(
            observation,
            EvolutionImprovementObservation,
        ):
            raise TypeError(
                "observation must be an "
                "EvolutionImprovementObservation"
            )

        target_component = (
            self._TARGET_COMPONENTS.get(
                observation.category
            )
        )

        if target_component is None:
            raise ValueError(
                "no target component is defined for "
                f"category: {observation.category}"
            )

        return EvolutionImprovementProposal(
            category=observation.category,
            problem=(
                "Repeated unsuccessful "
                f"{observation.category.value} "
                "experiences were observed."
            ),
            proposed_improvement=(
                "Review and improve the "
                f"{observation.category.value} "
                "process based on the observed evidence."
            ),
            evidence=(
                observation,
            ),
            target_component=target_component,
            expected_effect=(
                "Reduce repeated unsuccessful "
                f"{observation.category.value} "
                "outcomes."
            ),
        )