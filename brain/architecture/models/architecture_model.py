from dataclasses import dataclass


@dataclass(frozen=True)
class ArchitectureModel:
    """
    Represents the architectural structure of a codebase.
    """

    name: str

    pattern: str

    components: frozenset[str]

    layers: frozenset[str]