from dataclasses import dataclass


@dataclass(frozen=True)
class DataFlow:
    """
    Represents the movement of data between
    proposed system components.
    """

    source: str

    target: str

    data: str