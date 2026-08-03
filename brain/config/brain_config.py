from dataclasses import dataclass

from brain.embedding.embedding_pipeline import EmbeddingPipeline
from brain.registry.chunker_registry import ChunkerRegistry
from brain.registry.parser_registry import ParserRegistry
from brain.registry.reader_registry import ReaderRegistry


@dataclass(frozen=True)
class BrainConfig:

    reader_registry: ReaderRegistry

    parser_registry: ParserRegistry

    chunker_registry: ChunkerRegistry

    embedding_pipeline: EmbeddingPipeline