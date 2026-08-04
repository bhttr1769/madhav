from dataclasses import dataclass

from brain.search.services.semantic_searcher import SemanticSearcher
from brain.vector.search.vector_search import VectorSearch
from brain.vector.storage.vector_store import VectorStore
from core.ai.runtime.ai_runtime import AIRuntime


@dataclass(frozen=True)
class SearchRuntime:
    """
    Bundles all search-related services.
    """

    vector_search: VectorSearch

    semantic_searcher: SemanticSearcher


class SearchFactory:
    """
    Responsible for constructing the semantic search subsystem.
    """

    @staticmethod
    def create(
        runtime: AIRuntime,
        store: VectorStore,
    ) -> SearchRuntime:

        vector_search = VectorSearch(
            store,
        )

        semantic_searcher = SemanticSearcher(
            embedding_service=runtime.embedding,
            vector_search=vector_search,
        )

        return SearchRuntime(
            vector_search=vector_search,
            semantic_searcher=semantic_searcher,
        )