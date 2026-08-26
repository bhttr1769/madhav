from dataclasses import dataclass


@dataclass(frozen=True)
class Layer:
    """
    Represents a logical architectural layer.
    """

    name: str

    components: frozenset[str]

    confidence: float