from dataclasses import dataclass


@dataclass(frozen=True)
class DesignInterface:
    """
    Represents an interaction boundary between
    system components.
    """

    id: str

    name: str

    owner: str

    consumers: frozenset[str]

    purpose: str