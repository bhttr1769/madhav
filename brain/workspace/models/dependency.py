from dataclasses import dataclass


@dataclass(frozen=True)
class Dependency:
    """
    A project dependency.
    """

    name: str