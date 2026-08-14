from dataclasses import dataclass


@dataclass(frozen=True)
class Architecture:
    """
    Represents a detected architecture.
    """

    name: str