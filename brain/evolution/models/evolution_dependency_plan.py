from dataclasses import dataclass

from brain.evolution.models.evolution_dependency_requirement import (
    EvolutionDependencyRequirement,
)

from brain.evolution.models.evolution_dependency_resolution import (
    EvolutionDependencyResolution,
)

from brain.evolution.models.evolution_dependency_plan_operation import (
    EvolutionDependencyPlanOperation,
)


@dataclass(
    frozen=True,
)
class EvolutionDependencyPlan:
    """
    Represents the planned dependency change for
    an evolution.
    """

    requirement: EvolutionDependencyRequirement

    resolution: EvolutionDependencyResolution

    operation: EvolutionDependencyPlanOperation

    package_manager: str | None

    reason: str

    def __post_init__(
        self,
    ):
        if not isinstance(
            self.requirement,
            EvolutionDependencyRequirement,
        ):
            raise TypeError(
                "requirement must be an "
                "EvolutionDependencyRequirement"
            )

        if not isinstance(
            self.resolution,
            EvolutionDependencyResolution,
        ):
            raise TypeError(
                "resolution must be an "
                "EvolutionDependencyResolution"
            )

        if not isinstance(
            self.operation,
            EvolutionDependencyPlanOperation,
        ):
            raise TypeError(
                "operation must be an "
                "EvolutionDependencyPlanOperation"
            )

        if (
            self.package_manager is not None
            and not isinstance(
                self.package_manager,
                str,
            )
        ):
            raise TypeError(
                "package_manager must be a string "
                "or None"
            )

        if self.package_manager == "":
            raise ValueError(
                "package_manager must not be empty"
            )

        if not isinstance(
            self.reason,
            str,
        ):
            raise TypeError(
                "reason must be a string"
            )

        if not self.reason:
            raise ValueError(
                "reason must not be empty"
            )