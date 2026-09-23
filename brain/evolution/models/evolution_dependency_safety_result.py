from dataclasses import dataclass

from brain.evolution.models.evolution_dependency_safety_status import (
    EvolutionDependencySafetyStatus,
)


@dataclass(
    frozen=True,
)
class EvolutionDependencySafetyResult:
    """
    Represents the safety decision for evolution
    dependency plans.
    """

    status: EvolutionDependencySafetyStatus

    reason: str

    def __post_init__(
        self,
    ):
        if not isinstance(
            self.status,
            EvolutionDependencySafetyStatus,
        ):
            raise TypeError(
                "status must be an "
                "EvolutionDependencySafetyStatus"
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

    @property
    def allowed(
        self,
    ) -> bool:
        return (
            self.status
            is EvolutionDependencySafetyStatus.ALLOWED
        )