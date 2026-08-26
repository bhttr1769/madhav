from dataclasses import dataclass


@dataclass(frozen=True)
class Module:
    """
    Represents a Python module.
    """

    name: str

    path: str

    imports: frozenset[str]

    classes: frozenset[str]

    functions: frozenset[str]