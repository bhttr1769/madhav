from dataclasses import dataclass


@dataclass(frozen=True)
class DesignComponent:
    """
    Represents a proposed architectural component
    in a system design.
    """

    id: str

    name: str

    responsibility: str

    layer: str

    interfaces: frozenset[str]