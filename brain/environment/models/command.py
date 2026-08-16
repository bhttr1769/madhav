from dataclasses import dataclass


@dataclass(
    frozen=True,
)
class Command:
    """
    Represents a terminal command.
    """

    value: str