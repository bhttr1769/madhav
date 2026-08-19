from dataclasses import dataclass


@dataclass(
    frozen=True,
)
class ProjectCommand:
    """
    Represents a single project command.
    """

    name: str

    command: str