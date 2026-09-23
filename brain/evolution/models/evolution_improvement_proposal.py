from dataclasses import dataclass

from brain.evolution.models.evolution_improvement_category import (
    EvolutionImprovementCategory,
)

from brain.evolution.models.evolution_improvement_observation import (
    EvolutionImprovementObservation,
)


@dataclass(
    frozen=True,
)
class EvolutionImprovementProposal:
    """
    Represents a proposed improvement to the
    evolution engine.
    """

    category: EvolutionImprovementCategory

    problem: str

    proposed_improvement: str

    evidence: tuple[
        EvolutionImprovementObservation,
        ...
    ]

    target_component: str

    expected_effect: str

    def __post_init__(
        self,
    ):
        if not isinstance(
            self.category,
            EvolutionImprovementCategory,
        ):
            raise TypeError(
                "category must be an "
                "EvolutionImprovementCategory"
            )

        if not isinstance(
            self.problem,
            str,
        ):
            raise TypeError(
                "problem must be a string"
            )

        if not self.problem:
            raise ValueError(
                "problem must not be empty"
            )

        if not isinstance(
            self.proposed_improvement,
            str,
        ):
            raise TypeError(
                "proposed_improvement must be a string"
            )

        if not self.proposed_improvement:
            raise ValueError(
                "proposed_improvement must not be empty"
            )

        if not isinstance(
            self.evidence,
            tuple,
        ):
            raise TypeError(
                "evidence must be a tuple"
            )

        for observation in self.evidence:
            if not isinstance(
                observation,
                EvolutionImprovementObservation,
            ):
                raise TypeError(
                    "evidence must contain only "
                    "EvolutionImprovementObservation "
                    "instances"
                )

        if not self.evidence:
            raise ValueError(
                "evidence must not be empty"
            )

        if not isinstance(
            self.target_component,
            str,
        ):
            raise TypeError(
                "target_component must be a string"
            )

        if not self.target_component:
            raise ValueError(
                "target_component must not be empty"
            )

        if not isinstance(
            self.expected_effect,
            str,
        ):
            raise TypeError(
                "expected_effect must be a string"
            )

        if not self.expected_effect:
            raise ValueError(
                "expected_effect must not be empty"
            )