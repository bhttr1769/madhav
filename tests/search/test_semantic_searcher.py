from brain.search.models.search_result import SearchResult
from brain.vector.models.vector import Vector
from brain.vector.models.vector_record import VectorRecord
from brain.search.models.search_query import SearchQuery
from brain.search.services.semantic_searcher import SemanticSearcher




class FakeEmbeddingService:

    def embed(self, text: str):

        return [1.0, 0.0]


class FakeVectorSearch:

    def search(
        self,
        query,
    ):

        return [
            SearchResult(
                record=VectorRecord(
                    id="1",
                    vector=Vector([1.0, 0.0]),
                    document_id="doc",
                    chunk_id=0,
                ),
                score=0.95,
            )
        ]



def test_semantic_search():

    searcher = SemanticSearcher(
        embedding_service=FakeEmbeddingService(),
        vector_search=FakeVectorSearch(),
    )

    results = searcher.search(
        SearchQuery("hello")
    )

    assert len(results) == 1

    assert results[0].record.id == "1"

    assert results[0].score == 0.95