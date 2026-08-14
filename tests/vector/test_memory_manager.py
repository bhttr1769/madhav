from brain.memory.memory_manager import (
    MemoryManager,
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


def test_forget_document():

    store = VectorStore()

    store.add(
        VectorRecord(
            id="1",
            vector=Vector([1.0]),
            document_id="java.pdf",
            chunk_id=0,
            text="chunk",
        )
    )

    manager = MemoryManager(
        store,
    )

    assert manager.forget(
        "java.pdf"
    )

    assert not store.has_document(
        "java.pdf"
    )


def test_forget_unknown_document():

    store = VectorStore()

    manager = MemoryManager(
        store,
    )

    assert not manager.forget(
        "unknown.pdf"
    )