from dataclasses import dataclass

from brain.evolution.models.evolution_dependency_assessment import (
    EvolutionDependencyAssessment,
)

from brain.evolution.models.evolution_dependency_resolution_status import (
    EvolutionDependencyResolutionStatus,
)


@dataclass(
    frozen=True,
)
class EvolutionDependencyResolution:
    """
    Represents the resolution decision for an
    evolution dependency.
    """

    assessment: EvolutionDependencyAssessment

    status: EvolutionDependencyResolutionStatus

    package_manager: str | None

    reason: str

    def __post_init__(
        self,
    ):
        if not isinstance(
            self.assessment,
            EvolutionDependencyAssessment,
        ):
            raise TypeError(
                "assessment must be an "
                "EvolutionDependencyAssessment"
            )

        if not isinstance(
            self.status,
            EvolutionDependencyResolutionStatus,
        ):
            raise TypeError(
                "status must be an "
                "EvolutionDependencyResolutionStatus"
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

        if (
            self.package_manager == ""
        ):
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