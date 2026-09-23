from dataclasses import dataclass

from brain.package_managers.models.dependency import (
    Dependency,
)


@dataclass(
    frozen=True,
)
class EvolutionDependencyRequirement:
    """
    Represents a dependency required by an evolution.
    """

    dependency: Dependency

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