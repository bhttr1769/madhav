from dataclasses import dataclass

from brain.perception.models.observation import (
    Observation,
)


@dataclass(frozen=True)
class FeedbackResult:
    """
    Represents the result of comparing an expected
    outcome with observed state.
    """

    status: str
    expected: frozenset[Observation]
    observed: frozenset[Observation]

    def __post_init__(self) -> None:
        if not isinstance(
            self.status,
            str,
        ):
            raise TypeError(
                "status must be a string"
            )

        if not self.status.strip():
            raise ValueError(
                "status must not be empty"
            )

        if not isinstance(
            self.expected,
            frozenset,
        ):
            raise TypeError(
                "expected must be a frozenset"
            )

        if not isinstance(
            self.observed,
            frozenset,
        ):
            raise TypeError(
                "observed must be a frozenset"
            )

        for observation in (
            self.expected
            | self.observed
        ):
            if not isinstance(
                observation,
                Observation,
            ):
                raise TypeError(
                    "expected and observed must contain "
                    "only Observation instances"
                )