from dataclasses import dataclass


@dataclass(
    frozen=True,
)
class GitStatus:
    """
    Represents a Git working tree status.
    """

    is_clean: bool