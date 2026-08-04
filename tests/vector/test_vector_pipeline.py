from pathlib import Path

from brain.vector.models.vector import Vector
from brain.vector.models.vector_record import (
    VectorRecord,
)
from brain.vector.persistence.vector_serializer import (
    VectorSerializer,
)
from brain.vector.search.vector_search import (
    VectorSearch,
)
from brain.vector.storage.vector_store import (
    VectorStore,
)


def test_complete_vector_pipeline(
    tmp_path: Path,
):

    store = VectorStore()

    store.add(
        VectorRecord(
            id="1",
            vector=Vector([1.0, 0.0]),
            document_id="doc",
            chunk_id=0,
        )
    )

    store.add(
        VectorRecord(
            id="2",
            vector=Vector([0.0, 1.0]),
            document_id="doc",
            chunk_id=1,
        )
    )

    file_path = tmp_path / "vectors.json"

    VectorSerializer.save(
        store,
        str(file_path),
    )

    loaded_store = VectorSerializer.load(
        str(file_path),
    )

    search = VectorSearch(
        loaded_store,
    )

    results = search.search(
        Vector([1.0, 0.0])
    )

    assert len(results) == 2

    assert results[0].record.id == "1"