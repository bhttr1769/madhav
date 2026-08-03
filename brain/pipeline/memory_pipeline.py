from brain.vector.models.vector import Vector
from brain.vector.models.vector_record import VectorRecord
from brain.vector.storage.vector_store import VectorStore


class MemoryPipeline:
    """
    Builds semantic memory from processed documents.
    """

    def __init__(
        self,
        store: VectorStore,
    ):
        self._store = store

    def ingest(
        self,
        document,
    ) -> None:
        """
        Stores the embeddings of a processed document
        inside the vector database.
        """

        for index, chunk in enumerate(document.chunks):

            if chunk.embedding is None:
                raise ValueError(
                    f"Chunk {chunk.id} has no embedding."
                )

            record = VectorRecord(
                id=f"{document.name}:{index}",
                vector=Vector(chunk.embedding),
                document_id=document.name,
                chunk_id=index,
                metadata=document.metadata,
            )

            self._store.add(record)