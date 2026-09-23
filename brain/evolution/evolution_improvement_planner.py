from brain.evolution.models.evolution_improvement_category import (
    EvolutionImprovementCategory,
)

from brain.evolution.models.evolution_improvement_plan import (
    EvolutionImprovementPlan,
)

from brain.evolution.models.evolution_improvement_proposal import (
    EvolutionImprovementProposal,
)


class EvolutionImprovementPlanner:
    """
    Converts an improvement proposal into a
    structured implementation plan.

    This component plans an improvement but does
    not execute it.
    """

    _IMPLEMENTATION_DIRECTIONS = {
        EvolutionImprovementCategory.REQUIREMENT_UNDERSTANDING:
            "review and improve requirement understanding",

        EvolutionImprovementCategory.TASK_DECOMPOSITION:
            "review and improve task decomposition",

        EvolutionImprovementCategory.SYSTEM_DESIGN:
            "review and improve system design",

        EvolutionImprovementCategory.ENGINEERING_PLANNING:
            "review and improve engineering planning",

        EvolutionImprovementCategory.CODE_GENERATION:
            "review and improve code generation",

        EvolutionImprovementCategory.TEST_GENERATION:
            "review and improve test generation",

        EvolutionImprovementCategory.VERIFICATION:
            "review and improve verification",

        EvolutionImprovementCategory.DEBUGGING:
            "review and improve debugging",

        EvolutionImprovementCategory.REFACTORING:
            "review and improve refactoring",

        EvolutionImprovementCategory.CAPABILITY_DISCOVERY:
            "review and improve capability discovery",

        EvolutionImprovementCategory.CAPABILITY_INTEGRATION:
            "review and improve capability integration",

        EvolutionImprovementCategory.DEPENDENCY_MANAGEMENT:
            "review and improve dependency management",

        EvolutionImprovementCategory.SAFETY:
            "review and improve safety",

        EvolutionImprovementCategory.RECOVERY:
            "review and improve recovery",

        EvolutionImprovementCategory.ORCHESTRATION:
            "review and improve orchestration",
    }

    def plan(
        self,
        proposal: EvolutionImprovementProposal,
    ) -> EvolutionImprovementPlan:
        if not isinstance(
            proposal,
            EvolutionImprovementProposal,
        ):
            raise TypeError(
                "proposal must be an "
                "EvolutionImprovementProposal"
            )

        implementation_direction = (
            self._IMPLEMENTATION_DIRECTIONS.get(
                proposal.category
            )
        )

        if implementation_direction is None:
            raise ValueError(
                "no implementation direction is defined "
                "for category: "
                f"{proposal.category}"
            )

        return EvolutionImprovementPlan(
            proposal=proposal,
            category=proposal.category,
            target_component=proposal.target_component,
            implementation_direction=(
                implementation_direction
            ),
            reuse_existing=(
                "Reuse the existing target component "
                "and its current interfaces before "
                "introducing new components."
            ),
            constraints=(
                "Preserve existing behavior outside "
                "the identified improvement area.",
                "Do not introduce speculative abstractions.",
                "Preserve existing architectural boundaries.",
                "Validate the improvement before integration.",
            ),
            required_engineering_work=(
                "Inspect the existing target component.",
                "Identify the implementation area "
                "supported by the evidence.",
                "Design the smallest change required "
                "to address the observed problem.",
                "Generate and validate the required tests.",
                "Verify that existing behavior has "
                "not regressed.",
            ),
        )