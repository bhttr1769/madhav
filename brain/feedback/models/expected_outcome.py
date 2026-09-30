from dataclasses import dataclass

from brain.perception.models.observation import (
    Observation,
)


@dataclass(frozen=True)
class ExpectedOutcome:
    """
    Represents the observations expected after
    an action has been performed.
    """

    observations: frozenset[Observation]

    def __post_init__(self) -> None:
        if not isinstance(
            self.observations,
            frozenset,
        ):
            raise TypeError(
                "observations must be a frozenset"
            )

        for observation in self.observations:
            if not isinstance(
                observation,
                Observation,
            ):
                raise TypeError(
                    "observations must contain only "
                    "Observation instances"
                )