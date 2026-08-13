from brain.config.brain_config import BrainConfig
from brain.registry.reader_registry import ReaderRegistry
from brain.registry.parser_registry import ParserRegistry
from brain.registry.chunker_registry import ChunkerRegistry
from brain.config.embedding_config import EmbeddingConfig
from brain.factories.embedding_factory import EmbeddingFactory
from brain.embedding.embedding_pipeline import EmbeddingPipeline
from tests.utils.fake_rag_service import FakeRagService
from brain.graph.persistence.graph_manager import (
    GraphManager,
)


class FakeSearcher:
    def search(self, query):
        return []
    
class FakeMemoryPipeline:
    def ingest(self, document):
        pass

class FakeMemoryManager:

    def save(self, store):
        pass


class FakeMemoryRuntime:

    def __init__(self):

        self.store = None

        self.manager = FakeMemoryManager()

class FakeEntityPipeline:
    def process(self, document):
        pass

class FakeRelationshipPipeline:
    def process(self, document):
        pass


def test_brain_config_creation():
    config = BrainConfig(
        reader_registry=ReaderRegistry(),
        parser_registry=ParserRegistry(),
        chunker_registry=ChunkerRegistry(),
        embedding_pipeline=EmbeddingPipeline(
            EmbeddingFactory.create(
                EmbeddingConfig()
            )
        ),
        memory_pipeline=FakeMemoryPipeline(),
        memory_runtime=FakeMemoryRuntime(),
        semantic_searcher=FakeSearcher(),
        entity_pipeline=FakeEntityPipeline(),
        relationship_pipeline=FakeRelationshipPipeline(),
        graph_manager=GraphManager("tests/data/graph.json",),
        rag_service=FakeRagService(),
    )

    assert isinstance(config.reader_registry, ReaderRegistry)
    assert isinstance(config.parser_registry, ParserRegistry)
    assert isinstance(config.chunker_registry, ChunkerRegistry)