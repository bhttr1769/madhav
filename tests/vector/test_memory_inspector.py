from brain.memory.memory_inspector import (
    MemoryInspector,
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


def test_memory_inspector():

    store = VectorStore()

    record = VectorRecord(
        id="1",
        vector=Vector([1.0]),
        document_id="java.pdf",
        chunk_id=0,
        text="Hello Java",
    )

    store.add(record)

    inspector = MemoryInspector(
        store,
    )

    records = inspector.records()

    assert len(records) == 1

    assert records[0].document_id == "java.pdf"

    assert records[0].text == "Hello Java"