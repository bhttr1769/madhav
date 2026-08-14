from brain.memory.memory_rebuilder import (
    MemoryRebuilder,
)
from brain.vector.storage.vector_store import (
    VectorStore,
)


class FakePersistentMemoryManager:

    def load(
        self,
    ):

        return VectorStore()


def test_memory_rebuilder():

    manager = FakePersistentMemoryManager()

    rebuilder = MemoryRebuilder(
        manager,
    )

    store = rebuilder.rebuild()

    assert isinstance(
        store,
        VectorStore,
    )