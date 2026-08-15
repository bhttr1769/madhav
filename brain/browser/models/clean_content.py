from dataclasses import dataclass


@dataclass(
    frozen=True,
)
class CleanContent:
    """
    Normalized content.
    """

    text: str