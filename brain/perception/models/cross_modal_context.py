from dataclasses import dataclass

from brain.perception.models.observation import (
    Observation,
)


@dataclass(frozen=True)
class CrossModalContext:
    """
    Represents relationships discovered between
    observations from different perception sources.
    """

    observations: frozenset[Observation]

    relationships: frozenset[
        tuple[str, str, str]
    ]