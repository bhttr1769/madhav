from dataclasses import dataclass


@dataclass(
    frozen=True,
)
class GitStatus:
    """
    Represents the current state
    of a Git repository.
    """

    branch: str

    has_uncommitted_changes: bool

    has_untracked_files: bool