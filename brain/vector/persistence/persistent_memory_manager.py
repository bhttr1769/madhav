import os

from brain.vector.persistence.vector_serializer import (
    VectorSerializer,
)
from brain.vector.storage.vector_store import (
    VectorStore,
)


class PersistentMemoryManager:

    def __init__(
        self,
        path: str,
    ):
        self._path = path

    def exists(
        self,
    ) -> bool:

        return os.path.exists(
            self._path
        )

    def load(
        self,
    ) -> VectorStore:

        if not self.exists():

            return VectorStore()

        return VectorSerializer.load(
            self._path
        )

    def save(
        self,
        store: VectorStore,
    ) -> None:

        VectorSerializer.save(
            store,
            self._path,
        )