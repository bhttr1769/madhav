from brain.config.embedding_config import EmbeddingConfig
from brain.factories.embedding_factory import EmbeddingFactory
from brain.config.brain_config import BrainConfig
from brain.manager import BrainManager
from brain.registry.chunker_registry import ChunkerRegistry
from brain.registry.parser_registry import ParserRegistry
from brain.registry.reader_registry import ReaderRegistry
from brain.embedding.embedding_pipeline import EmbeddingPipeline

class BrainFactory:
    """
    Responsible for creating fully configured BrainManager instances.
    """

    @staticmethod
    def create() -> BrainManager:
        config = BrainConfig(
            reader_registry=ReaderRegistry(),
            parser_registry=ParserRegistry(),
            chunker_registry=ChunkerRegistry(),
            embedding_pipeline=EmbeddingPipeline(
                EmbeddingFactory.create(
                    EmbeddingConfig()
                )
            ),
        )

        return BrainManager(config)