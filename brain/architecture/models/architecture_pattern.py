from dataclasses import dataclass


@dataclass(frozen=True)
class ArchitecturePattern:
    """
    Represents an inferred architectural pattern.
    """

    name: str

    confidence: float

    evidence: frozenset[str]