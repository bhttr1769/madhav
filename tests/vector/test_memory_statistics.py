from brain.memory.memory_statistics import (
    MemoryStatistics,
)
from brain.vector.models.vector import Vector
from brain.vector.models.vector_record import (
    VectorRecord,
)
from brain.vector.storage.vector_store import (
    VectorStore,
)


def test_memory_statistics():

    store = VectorStore()

    store.add(
        VectorRecord(
            id="1",
            vector=Vector([1.0]),
            document_id="doc1",
            chunk_id=0,
            text="chunk1",
        )
    )

    store.add(
        VectorRecord(
            id="2",
            vector=Vector([2.0]),
            document_id="doc1",
            chunk_id=1,
            text="chunk2",
        )
    )

    store.add(
        VectorRecord(
            id="3",
            vector=Vector([3.0]),
            document_id="doc2",
            chunk_id=0,
            text="chunk3",
        )
    )

    stats = MemoryStatistics(
        store,
    )

    assert stats.document_count() == 2

    assert stats.chunk_count() == 3

    assert stats.vector_count() == 3