from dataclasses import dataclass

from brain.perception.models.observation import (
    Observation,
)


@dataclass(frozen=True)
class ObservationTransition:
    """
    Represents the environmental observations immediately
    before and after an external action has been performed.
    """

    before: frozenset[Observation]
    after: frozenset[Observation]

    def __post_init__(self) -> None:
        if not isinstance(
            self.before,
            frozenset,
        ):
            raise TypeError(
                "before must be a frozenset"
            )

        if not isinstance(
            self.after,
            frozenset,
        ):
            raise TypeError(
                "after must be a frozenset"
            )

        for observation in (
            self.before
            | self.after
        ):
            if not isinstance(
                observation,
                Observation,
            ):
                raise TypeError(
                    "before and after must contain only "
                    "Observation instances"
                )