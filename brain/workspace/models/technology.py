from dataclasses import dataclass


@dataclass(frozen=True)
class Technology:
    """
    A detected technology.
    """

    name: str

    category: str