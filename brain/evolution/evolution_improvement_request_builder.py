from brain.evolution.models.evolution_improvement_plan import (
    EvolutionImprovementPlan,
)

from brain.evolution.models.evolution_request import (
    EvolutionRequest,
)


class EvolutionImprovementRequestBuilder:
    """
    Converts an EvolutionImprovementPlan into the
    EvolutionRequest understood by the existing
    evolution pipeline.

    This component only translates planning information.
    It does not execute evolution.
    """

    def build(
        self,
        plan: EvolutionImprovementPlan,
        mode: str = "supervised",
    ) -> EvolutionRequest:
        if not isinstance(
            plan,
            EvolutionImprovementPlan,
        ):
            raise TypeError(
                "plan must be an "
                "EvolutionImprovementPlan"
            )

        if not isinstance(
            mode,
            str,
        ):
            raise TypeError(
                "mode must be a string"
            )

        if not mode:
            raise ValueError(
                "mode must not be empty"
            )

        objective = (
            f"Improve {plan.target_component}: "
            f"{plan.proposal.proposed_improvement}. "
            f"Problem: {plan.proposal.problem}. "
            f"Expected effect: "
            f"{plan.proposal.expected_effect}."
        )

        constraints = frozenset(
            plan.constraints
            + (
                f"Target component: "
                f"{plan.target_component}",
                f"Implementation direction: "
                f"{plan.implementation_direction}",
                f"Reuse strategy: "
                f"{plan.reuse_existing}",
            )
        )

        return EvolutionRequest(
            requested_capability=(
                plan.target_component
            ),
            objective=objective,
            constraints=constraints,
            mode=mode,
        )