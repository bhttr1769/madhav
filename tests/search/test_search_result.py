from brain.search.models.search_result import SearchResult
from brain.vector.models.vector import Vector
from brain.vector.models.vector_record import VectorRecord


def test_search_result():

    record = VectorRecord(
        id="1",
        vector=Vector([1.0]),
        document_id="doc",
        chunk_id=0,
        text="Hello World",
    )

    result = SearchResult(
        record=record,
        score=0.95,
    )

    assert result.score == 0.95
    assert result.record.id == "1"