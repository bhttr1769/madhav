from dataclasses import dataclass

from brain.vector.models.vector_record import VectorRecord


@dataclass(frozen=True)
class SearchResult:
    """
    Represents one semantic search result.
    """

    record: VectorRecord

    score: float