from dataclasses import dataclass

from brain.evolution.models.evolution_improvement_category import (
    EvolutionImprovementCategory,
)

from brain.evolution.models.evolution_improvement_proposal import (
    EvolutionImprovementProposal,
)


@dataclass(
    frozen=True,
)
class EvolutionImprovementPlan:
    """
    Represents a structured implementation plan for
    an evolution improvement proposal.
    """

    proposal: EvolutionImprovementProposal

    category: EvolutionImprovementCategory

    target_component: str

    implementation_direction: str

    reuse_existing: str

    constraints: tuple[
        str,
        ...
    ]

    required_engineering_work: tuple[
        str,
        ...
    ]

    def __post_init__(
        self,
    ):
        if not isinstance(
            self.proposal,
            EvolutionImprovementProposal,
        ):
            raise TypeError(
                "proposal must be an "
                "EvolutionImprovementProposal"
            )

        if not isinstance(
            self.category,
            EvolutionImprovementCategory,
        ):
            raise TypeError(
                "category must be an "
                "EvolutionImprovementCategory"
            )

        if self.category is not self.proposal.category:
            raise ValueError(
                "category must match proposal.category"
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

        if (
            self.target_component
            != self.proposal.target_component
        ):
            raise ValueError(
                "target_component must match "
                "proposal.target_component"
            )

        if not isinstance(
            self.implementation_direction,
            str,
        ):
            raise TypeError(
                "implementation_direction must be a string"
            )

        if not self.implementation_direction:
            raise ValueError(
                "implementation_direction must not "
                "be empty"
            )

        if not isinstance(
            self.reuse_existing,
            str,
        ):
            raise TypeError(
                "reuse_existing must be a string"
            )

        if not self.reuse_existing:
            raise ValueError(
                "reuse_existing must not be empty"
            )

        if not isinstance(
            self.constraints,
            tuple,
        ):
            raise TypeError(
                "constraints must be a tuple"
            )

        for constraint in self.constraints:
            if not isinstance(
                constraint,
                str,
            ):
                raise TypeError(
                    "constraints must contain only strings"
                )

            if not constraint:
                raise ValueError(
                    "constraints must not contain "
                    "empty strings"
                )

        if not self.constraints:
            raise ValueError(
                "constraints must not be empty"
            )

        if not isinstance(
            self.required_engineering_work,
            tuple,
        ):
            raise TypeError(
                "required_engineering_work must be a tuple"
            )

        for work_item in self.required_engineering_work:
            if not isinstance(
                work_item,
                str,
            ):
                raise TypeError(
                    "required_engineering_work must "
                    "contain only strings"
                )

            if not work_item:
                raise ValueError(
                    "required_engineering_work must not "
                    "contain empty strings"
                )

        if not self.required_engineering_work:
            raise ValueError(
                "required_engineering_work must not "
                "be empty"
            )