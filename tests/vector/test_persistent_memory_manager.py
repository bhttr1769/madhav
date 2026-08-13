from brain.vector.persistence.persistent_memory_manager import (
    PersistentMemoryManager,
)

from brain.vector.models.vector import Vector

from brain.vector.models.vector_record import (
    VectorRecord,
)


def test_load_returns_empty_store_when_file_does_not_exist():

    manager = PersistentMemoryManager(
        "missing.json"
    )

    store = manager.load()

    assert store.count() == 0


def test_save_and_load(tmp_path):

    path = tmp_path / "memory.json"

    manager = PersistentMemoryManager(
        str(path)
    )

    record = VectorRecord(
        id="1",
        vector=Vector([0.1]),
        document_id="doc",
        chunk_id=0,
        text="Java",
    )

    store = manager.load()

    store.add(record)

    manager.save(store)

    loaded_store = manager.load()

    assert loaded_store.count() == 1