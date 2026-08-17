from dataclasses import dataclass


@dataclass(
    frozen=True,
)
class GitBranch:
    """
    Represents a Git branch.
    """

    name: str