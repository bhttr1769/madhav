from dataclasses import dataclass


@dataclass(
    frozen=True,
)
class Signature:
    """
    A detectable workspace artifact.
    """

    value: str

    category: str

    path: str