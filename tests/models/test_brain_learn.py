from pathlib import Path

from brain.config.brain_config import BrainConfig
from brain.manager import BrainManager
from brain.models.document import Document
from brain.registry.chunker_registry import ChunkerRegistry
from brain.registry.parser_registry import ParserRegistry
from brain.registry.reader_registry import ReaderRegistry
from tests.utils.fake_rag_service import FakeRagService
from brain.graph.persistence.graph_manager import (
    GraphManager,
)
from brain.graph.storage.graph_store import (
    GraphStore,
)


class FakeEmbeddingPipeline:
    def process(self, document):
        return document


class FakeMemoryPipeline:

    def __init__(self):
        self.ingested = False

    def ingest(self, document):
        self.ingested = True

class FakeMemoryManager:

    def save(self, store):
        pass


class FakeMemoryRuntime:

    def __init__(self):

        self.store = None

        self.manager = FakeMemoryManager()

class FakeSearcher:
    def search(self, query):
        return []


class FakeStore(GraphStore):
    pass


class FakeEntityPipeline:

    def __init__(self):

        self._store = FakeStore()

    def process(
        self,
        document,
    ):
        pass

class FakeRelationshipPipeline:

    def __init__(self):
        self.called = False

    def process(self, document):
        self.called = True

class FakeBrain(BrainManager):

    def read(self, file_path):
        return Document(
            name="sample.txt",
            path=Path("sample.txt"),
            extension=".txt",
            content="Hello",
            size=5,
            created_at=None,
            modified_at=None,
        )


def test_brain_learn():

    memory = FakeMemoryPipeline()
    relationship_pipeline = FakeRelationshipPipeline()

    config = BrainConfig(
        reader_registry=ReaderRegistry(),
        parser_registry=ParserRegistry(),
        chunker_registry=ChunkerRegistry(),
        embedding_pipeline=FakeEmbeddingPipeline(),
        memory_pipeline=memory,
        memory_runtime=FakeMemoryRuntime(),
        semantic_searcher=FakeSearcher(),
        entity_pipeline=FakeEntityPipeline(),
        relationship_pipeline=relationship_pipeline,
        graph_manager=GraphManager("tests/data/graph.json",),
        rag_service=FakeRagService(),
    )

    brain = FakeBrain(config)

    brain.learn("sample.txt")

    assert memory.ingested

    assert relationship_pipeline.called