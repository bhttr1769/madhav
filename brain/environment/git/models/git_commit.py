from dataclasses import dataclass


@dataclass(
    frozen=True,
)
class GitCommit:
    """
    Represents a Git commit.
    """

    hash: str