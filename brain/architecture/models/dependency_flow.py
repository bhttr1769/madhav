from dataclasses import dataclass


@dataclass(frozen=True)
class DependencyFlow:
    """
    Represents a dependency relationship between
    architectural components.
    """

    source: str

    target: str

    imports: frozenset[str]