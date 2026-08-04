from dataclasses import dataclass


@dataclass(frozen=True)
class SearchQuery:
    """
    Represents a semantic search request.
    """

    text: str

    top_k: int = 5

    min_score: float = 0.0