from dataclasses import dataclass


@dataclass(frozen=True)
class CodeChange:
    """
    Represents a proposed change to the codebase.
    """

    path: str

    operation: str

    content: str