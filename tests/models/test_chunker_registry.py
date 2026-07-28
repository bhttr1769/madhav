from brain.chunking.fixed_chunker import FixedChunker
from brain.registry.chunker_registry import ChunkerRegistry


def test_chunker_registry_returns_default_chunker():

    registry = ChunkerRegistry()

    chunker = registry.get_chunker()

    assert isinstance(chunker, FixedChunker)