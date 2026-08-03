from datetime import datetime
from pathlib import Path

from brain.models.chunk import Chunk
from brain.models.document import Document
from brain.pipeline.memory_pipeline import MemoryPipeline
from brain.vector.storage.vector_store import VectorStore


def test_memory_pipeline_ingests_document():

    document = Document(
        name="sample.txt",
        path=Path("sample.txt"),
        extension=".txt",
        content="Hello Madhav!",
        size=13,
        created_at=datetime.now(),
        modified_at=datetime.now(),
    )

    document.metadata = {}

    document.chunks = [
        Chunk(
            id=0,
            text="Hello Madhav!",
            start_char=0,
            end_char=13,
            token_count=2,
            embedding=[1.0, 2.0, 3.0],
        )
    ]

    store = VectorStore()

    pipeline = MemoryPipeline(
        store=store,
    )

    pipeline.ingest(document)

    assert store.count() == 1

    record = store.get("sample.txt:0")

    assert record is not None
    assert record.document_id == "sample.txt"
    assert record.chunk_id == 0
    assert record.vector.values == [1.0, 2.0, 3.0]