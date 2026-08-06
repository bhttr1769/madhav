from brain.vector.models.vector import Vector
from brain.vector.models.vector_record import VectorRecord


def test_vector_record_creation():

    record = VectorRecord(
        id="1",
        vector=Vector([1.0, 2.0]),
        document_id="doc1",
        chunk_id=5,
        text="Hello World",
    )

    assert record.id == "1"

    assert record.document_id == "doc1"

    assert record.chunk_id == 5

    assert record.vector.dimensions == 2

    assert record.metadata == {}