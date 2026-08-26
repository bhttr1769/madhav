from dataclasses import dataclass


@dataclass(frozen=True)
class ClassModel:
    """
    Represents a Python class.
    """

    name: str

    module: str

    bases: frozenset[str]

    methods: frozenset[str]