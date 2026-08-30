from dataclasses import dataclass


@dataclass(frozen=True)
class DesignDependency:
    """
    Represents a dependency between proposed
    system components.
    """

    source: str

    target: str

    reason: str