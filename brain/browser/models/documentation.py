from dataclasses import dataclass


@dataclass(
    frozen=True,
)
class Documentation:
    """
    Structured documentation.
    """

    sections: list[str]