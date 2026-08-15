from dataclasses import dataclass


@dataclass(
    frozen=True,
)
class ExtractedContent:
    """
    Extracted document content.
    """

    text: str