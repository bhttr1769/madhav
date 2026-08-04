from brain.vector.models.vector import Vector
from brain.vector.models.vector_record import VectorRecord
from brain.vector.similarity.cosine_similarity import (
    CosineSimilarity,
)
from brain.vector.storage.vector_store import VectorStore
from brain.search.models.search_result import SearchResult


class VectorSearch:
    """
    Performs similarity search over a vector store.
    """

    def __init__(
        self,
        store: VectorStore,
    ):
        self._store = store

    def search(
        self,
        query: Vector,
    ) -> list[SearchResult]:
        """
        Return the most similar vector records.
        """

        scored_records = []

        for record in self._store.all():

            score = CosineSimilarity.compute(
                query,
                record.vector,
            )

            scored_records.append(
                (score, record)
            )

        scored_records.sort(
            key=lambda item: item[0],
            reverse=True,
        )

        results = []

        for score, record in scored_records:

            results.append(
                SearchResult(
                    record=record,
                    score=score,
                )
            )

        return results