import json

from brain.vector.models.vector import Vector
from brain.vector.models.vector_record import (
    VectorRecord,
)
from brain.vector.storage.vector_store import (
    VectorStore,
)


class VectorSerializer:
    """
    Saves and loads vector stores.
    """

    @staticmethod
    def save(
        store: VectorStore,
        path: str,
    ) -> None:

        data = []

        for record in store.all():

            data.append(
                {
                    "id": record.id,
                    "vector": record.vector.values,
                    "document_id": record.document_id,
                    "chunk_id": record.chunk_id,
                    "text": record.text,
                    "metadata": record.metadata,
                }
            )

        with open(
            path,
            "w",
            encoding="utf-8",
        ) as file:

            json.dump(
                data,
                file,
                indent=4,
            )

    @staticmethod
    def load(
        path: str,
    ) -> VectorStore:

        store = VectorStore()

        with open(
            path,
            "r",
            encoding="utf-8",
        ) as file:

            data = json.load(file)

        for item in data:

            store.add(
                VectorRecord(
                    id=item["id"],
                    vector=Vector(
                        item["vector"]
                    ),
                    document_id=item["document_id"],
                    chunk_id=item["chunk_id"],
                    text=item["text"],
                    metadata=item["metadata"],
                )
            )

        return store