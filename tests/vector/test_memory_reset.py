from brain.memory.memory_reset import (
    MemoryReset,
)
from brain.vector.models.vector import (
    Vector,
)
from brain.vector.models.vector_record import (
    VectorRecord,
)
from brain.vector.storage.vector_store import (
    VectorStore,
)


def test_memory_reset():

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
            document_id="doc2",
            chunk_id=0,
            text="chunk2",
        )
    )

    reset = MemoryReset(
        store,
    )

    reset.clear()

    assert store.count() == 0