from dataclasses import dataclass

from brain.registry.reader_registry import ReaderRegistry
from brain.registry.parser_registry import ParserRegistry
from brain.registry.chunker_registry import ChunkerRegistry


@dataclass(frozen=True)
class BrainConfig:
    """
    Holds all dependencies required by BrainManager.
    """

    reader_registry: ReaderRegistry
    parser_registry: ParserRegistry
    chunker_registry: ChunkerRegistry