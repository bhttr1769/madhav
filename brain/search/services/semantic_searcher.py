from brain.search.models.search_query import SearchQuery
from brain.search.models.search_result import SearchResult
from brain.vector.models.vector import Vector
from brain.vector.search.vector_search import VectorSearch
from core.ai.services.embedding_service import EmbeddingService


class SemanticSearcher:
    """
    Performs semantic search over the vector database.
    """

    def __init__(
        self,
        embedding_service: EmbeddingService,
        vector_search: VectorSearch,
    ):
        self._embedding_service = embedding_service
        self._vector_search = vector_search

    def search(
        self,
        query: SearchQuery,
    ) -> list[SearchResult]:

        embedding = self._embedding_service.embed(
            query.text
        )

        results = self._vector_search.search(
            query=Vector(embedding),
        )

        results = [
            result
            for result in results
            if result.score >= query.min_score
        ]

        return results[:query.top_k]