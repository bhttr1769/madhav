from dataclasses import dataclass


@dataclass(frozen=True)
class File:
    """
    Represents a parsed repository file.
    """

    name: str

    path: str

    extension: str

    category: str

    metadata: frozenset[
        tuple[str, str]
    ]