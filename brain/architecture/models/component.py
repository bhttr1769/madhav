from dataclasses import dataclass


@dataclass(frozen=True)
class Component:
    """
    Represents a logical architectural component.
    """

    name: str

    path: str

    layer: str | None

    modules: frozenset[str]