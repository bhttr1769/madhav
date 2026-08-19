from dataclasses import dataclass


@dataclass(
    frozen=True,
)
class DependencyFile:
    """
    Represents a dependency manifest.
    """

    name: str

    path: str

    type: str