from dataclasses import dataclass

from brain.package_managers.models.dependency import (
    Dependency,
)

from brain.evolution.models.evolution_dependency_status import (
    EvolutionDependencyStatus,
)


@dataclass(
    frozen=True,
)
class EvolutionDependencyAssessment:
    """
    Represents the assessed state of an evolution dependency.
    """

    dependency: Dependency

    status: EvolutionDependencyStatus

    reason: str

    def __post_init__(
        self,
    ):

        if not isinstance(
            self.dependency,
            Dependency,
        ):
            raise TypeError(
                "dependency must be a Dependency"
            )

        if not isinstance(
            self.status,
            EvolutionDependencyStatus,
        ):
            raise TypeError(
                "status must be an "
                "EvolutionDependencyStatus"
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