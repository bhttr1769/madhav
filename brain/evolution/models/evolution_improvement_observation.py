from dataclasses import dataclass

from brain.evolution.models.evolution_improvement_category import (
    EvolutionImprovementCategory,
)


@dataclass(
    frozen=True,
)
class EvolutionImprovementObservation:
    """
    Represents evidence that may indicate an
    improvement opportunity in the evolution engine.
    """

    category: EvolutionImprovementCategory

    description: str

    evolution_ids: tuple[str, ...]

    occurrence_count: int

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
            self.description,
            str,
        ):
            raise TypeError(
                "description must be a string"
            )

        if not self.description:
            raise ValueError(
                "description must not be empty"
            )

        if not isinstance(
            self.evolution_ids,
            tuple,
        ):
            raise TypeError(
                "evolution_ids must be a tuple"
            )

        for evolution_id in self.evolution_ids:
            if not isinstance(
                evolution_id,
                str,
            ):
                raise TypeError(
                    "evolution_ids must contain only strings"
                )

            if not evolution_id:
                raise ValueError(
                    "evolution_ids must not contain "
                    "empty strings"
                )

        if not isinstance(
            self.occurrence_count,
            int,
        ):
            raise TypeError(
                "occurrence_count must be an integer"
            )

        if self.occurrence_count < 1:
            raise ValueError(
                "occurrence_count must be at least 1"
            )

        if (
            self.occurrence_count
            != len(self.evolution_ids)
        ):
            raise ValueError(
                "occurrence_count must match the number "
                "of evolution_ids"
            )