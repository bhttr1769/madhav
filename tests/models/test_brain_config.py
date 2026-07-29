from brain.config.brain_config import BrainConfig
from brain.registry.reader_registry import ReaderRegistry
from brain.registry.parser_registry import ParserRegistry
from brain.registry.chunker_registry import ChunkerRegistry


def test_brain_config_creation():
    config = BrainConfig(
        reader_registry=ReaderRegistry(),
        parser_registry=ParserRegistry(),
        chunker_registry=ChunkerRegistry(),
    )

    assert isinstance(config.reader_registry, ReaderRegistry)
    assert isinstance(config.parser_registry, ParserRegistry)
    assert isinstance(config.chunker_registry, ChunkerRegistry)