from dataclasses import dataclass


@dataclass(
    frozen=True,
)
class Dependency:
    """
    Represents a project dependency.
    """

    name: str

    version: str

    source: str
 
    metadata: frozenset[
        tuple[str, str]
    ] = frozenset()