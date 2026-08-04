from brain.config.brain_config import BrainConfig
from brain.embedding.embedding_pipeline import EmbeddingPipeline
from brain.manager import BrainManager
from brain.registry.chunker_registry import ChunkerRegistry
from brain.registry.parser_registry import ParserRegistry
from brain.registry.reader_registry import ReaderRegistry

from tests.embedding.fake_embedding import FakeEmbedding


class FakeSearcher:
    def search(self, query):
        return []
    
class FakeMemoryPipeline:
    def ingest(self, document):
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
            semantic_searcher=FakeSearcher(),
        )

        return BrainManager(config)