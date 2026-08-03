from brain.vector.models.vector import Vector
from brain.vector.models.vector_record import VectorRecord
from brain.vector.storage.vector_store import VectorStore


def create_record(record_id: str) -> VectorRecord:

    return VectorRecord(
        id=record_id,
        vector=Vector([1.0, 2.0, 3.0]),
        document_id="doc1",
        chunk_id=0,
    )


def test_add_record():

    store = VectorStore()

    record = create_record("1")

    store.add(record)

    assert store.count() == 1


def test_get_record():

    store = VectorStore()

    record = create_record("1")

    store.add(record)

    assert store.get("1") is record


def test_remove_record():

    store = VectorStore()

    record = create_record("1")

    store.add(record)

    store.remove("1")

    assert store.get("1") is None


def test_exists():

    store = VectorStore()

    record = create_record("1")

    store.add(record)

    assert store.exists("1")


def test_clear():

    store = VectorStore()

    store.add(create_record("1"))

    store.add(create_record("2"))

    store.clear()

    assert store.count() == 0