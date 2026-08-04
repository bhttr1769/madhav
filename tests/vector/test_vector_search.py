from brain.vector.models.vector import Vector
from brain.vector.models.vector_record import (
    VectorRecord,
)
from brain.vector.search.vector_search import (
    VectorSearch,
)
from brain.vector.storage.vector_store import (
    VectorStore,
)


def create_record(
    record_id: str,
    values: list[float],
):

    return VectorRecord(
        id=record_id,
        vector=Vector(values),
        document_id="doc",
        chunk_id=0,
    )


def test_returns_most_similar_vector():

    store = VectorStore()

    store.add(
        create_record(
            "A",
            [1.0, 0.0],
        )
    )

    store.add(
        create_record(
            "B",
            [0.0, 1.0],
        )
    )

    search = VectorSearch(store)

    results = search.search(
        Vector([1.0, 0.0])
    )

    assert results[0].record.id == "A"


def test_limit_results():

    store = VectorStore()

    for i in range(10):

        store.add(
            create_record(
                str(i),
                [1.0, float(i)],
            )
        )

    search = VectorSearch(store)

    results = search.search(
        Vector([1.0, 1.0]),
    )

    assert len(results) == 10

    assert results[0].score >= results[1].score
    assert results[1].score >= results[2].score


def test_empty_store():

    store = VectorStore()

    search = VectorSearch(store)

    results = search.search(
        Vector([1.0, 2.0])
    )

    assert results == []