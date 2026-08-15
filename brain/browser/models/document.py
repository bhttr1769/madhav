from dataclasses import dataclass


@dataclass(
    frozen=True,
)
class Document:
    """
    Parsed document.
    """

    title: str

    content: str