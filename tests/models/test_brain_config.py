from brain.config.brain_config import BrainConfig
from brain.registry.reader_registry import ReaderRegistry
from brain.registry.parser_registry import ParserRegistry
from brain.registry.chunker_registry import ChunkerRegistry
from brain.config.embedding_config import EmbeddingConfig
from brain.factories.embedding_factory import EmbeddingFactory
from brain.embedding.embedding_pipeline import EmbeddingPipeline


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
    )

    assert isinstance(config.reader_registry, ReaderRegistry)
    assert isinstance(config.parser_registry, ParserRegistry)
    assert isinstance(config.chunker_registry, ChunkerRegistry)