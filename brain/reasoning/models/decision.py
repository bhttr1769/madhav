from dataclasses import dataclass


@dataclass(frozen=True)
class Decision:
    """
    Represents a reasoning decision.
    """

    action: str

    rationale: str

    confidence: float

    alternatives: frozenset[str]