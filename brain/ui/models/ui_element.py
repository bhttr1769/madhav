from dataclasses import dataclass


@dataclass(frozen=True)
class UIElement:
    """
    Represents a detected user-interface element.
    """

    element_type: str

    name: str

    x: int

    y: int

    width: int

    height: int

    text: str | None = None

    confidence: float = 1.0