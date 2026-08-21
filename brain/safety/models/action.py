from dataclasses import dataclass


@dataclass(
    frozen=True,
)
class Action:
    """
    Represents an operation Madhav intends to perform.
    """

    name: str

    category: str

    target: str