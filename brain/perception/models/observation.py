from dataclasses import dataclass


@dataclass(frozen=True)
class Observation:
    """
    Represents an observation produced by a perception subsystem.
    """

    source: str

    category: str

    subject: str

    value: str

    confidence: float = 1.0