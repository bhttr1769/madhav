from dataclasses import dataclass

from brain.pipeline.memory_pipeline import MemoryPipeline
from brain.vector.storage.vector_store import VectorStore
from brain.vector.persistence.persistent_memory_manager import (
    PersistentMemoryManager,
)


@dataclass(frozen=True)
class MemoryRuntime:
    """
    Bundles all memory-related services.
    """

    store: VectorStore

    pipeline: MemoryPipeline

    manager: PersistentMemoryManager


class MemoryFactory:
    """
    Responsible for constructing the memory subsystem.
    """

    @staticmethod
    def create() -> MemoryRuntime:

        manager = PersistentMemoryManager(
            path="memory.json",
        )

        store = manager.load()

        pipeline = MemoryPipeline(
            store=store,
        )

        return MemoryRuntime(
            store=store,
            pipeline=pipeline,
            manager=manager,
        )