from brain.memory.memory_index import (
    MemoryIndex,
)
from brain.vector.models.vector import Vector
from brain.vector.models.vector_record import (
    VectorRecord,
)
from brain.vector.storage.vector_store import (
    VectorStore,
)


def test_memory_index():

    store = VectorStore()

    store.add(
        VectorRecord(
            id="1",
            vector=Vector([1.0]),
            document_id="spring.pdf",
            chunk_id=0,
            text="chunk",
        )
    )

    store.add(
        VectorRecord(
            id="2",
            vector=Vector([2.0]),
            document_id="java.pdf",
            chunk_id=0,
            text="chunk",
        )
    )

    index = MemoryIndex(
        store,
    )

    assert index.documents() == [
        "java.pdf",
        "spring.pdf",
    ]

    assert index.contains(
        "java.pdf"
    )

    assert not index.contains(
        "python.pdf"
    )