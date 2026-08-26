from dataclasses import dataclass


@dataclass(frozen=True)
class Directory:
    """
    Represents a parsed repository directory.
    """

    name: str

    path: str