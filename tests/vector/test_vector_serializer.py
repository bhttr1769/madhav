from pathlib import Path

from brain.vector.models.vector import Vector
from brain.vector.models.vector_record import (
    VectorRecord,
)
from brain.vector.persistence.vector_serializer import (
    VectorSerializer,
)
from brain.vector.storage.vector_store import (
    VectorStore,
)


def test_save_and_load_vector_store(
    tmp_path: Path,
):

    store = VectorStore()

    store.add(
        VectorRecord(
            id="1",
            vector=Vector([1.0, 2.0]),
            document_id="doc",
            chunk_id=0,
        )
    )

    file_path = tmp_path / "vectors.json"

    VectorSerializer.save(
        store,
        str(file_path),
    )

    loaded = VectorSerializer.load(
        str(file_path),
    )

    assert loaded.count() == 1

    record = loaded.get("1")

    assert record is not None

    assert record.vector.values == [1.0, 2.0]

    assert record.document_id == "doc"