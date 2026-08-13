from brain.config.brain_config import BrainConfig
from brain.embedding.embedding_pipeline import EmbeddingPipeline
from brain.manager import BrainManager
from brain.registry.chunker_registry import ChunkerRegistry
from brain.registry.parser_registry import ParserRegistry
from brain.registry.reader_registry import ReaderRegistry

from tests.embedding.fake_embedding import FakeEmbedding

from tests.utils.fake_rag_service import FakeRagService


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

class TestBrainFactory:
    """
    Factory used by unit tests.

    Uses fake dependencies so tests never depend on
    external AI providers.
    """

    @staticmethod
    def create() -> BrainManager:

        config = BrainConfig(
            reader_registry=ReaderRegistry(),
            parser_registry=ParserRegistry(),
            chunker_registry=ChunkerRegistry(),
            embedding_pipeline=EmbeddingPipeline(
                FakeEmbedding()
            ),
            memory_pipeline=FakeMemoryPipeline(),
            memory_runtime=FakeMemoryRuntime(),
            semantic_searcher=FakeSearcher(),
            entity_pipeline=FakeEntityPipeline(),
            relationship_pipeline=FakeRelationshipPipeline(),
            rag_service=FakeRagService(),
        )

        return BrainManager(config)