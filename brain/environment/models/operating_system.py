from dataclasses import dataclass


@dataclass(
    frozen=True,
)
class OperatingSystem:
    """
    Represents the current operating system.
    """

    name: str

    version: str