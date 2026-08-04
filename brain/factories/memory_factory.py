from dataclasses import dataclass

from brain.pipeline.memory_pipeline import MemoryPipeline
from brain.vector.storage.vector_store import VectorStore


@dataclass(frozen=True)
class MemoryRuntime:
    """
    Bundles all memory-related services.
    """

    store: VectorStore

    pipeline: MemoryPipeline


class MemoryFactory:
    """
    Responsible for constructing the memory subsystem.
    """

    @staticmethod
    def create() -> MemoryRuntime:

        store = VectorStore()

        pipeline = MemoryPipeline(
            store=store,
        )

        return MemoryRuntime(
            store=store,
            pipeline=pipeline,
        )