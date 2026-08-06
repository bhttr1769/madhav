from dataclasses import dataclass

from brain.graph.pipeline.entity_pipeline import EntityPipeline
from brain.embedding.embedding_pipeline import EmbeddingPipeline
from brain.registry.chunker_registry import ChunkerRegistry
from brain.registry.parser_registry import ParserRegistry
from brain.registry.reader_registry import ReaderRegistry
from brain.search.services.semantic_searcher import SemanticSearcher
from brain.pipeline.memory_pipeline import MemoryPipeline
from brain.graph.pipeline.relationship_pipeline import (
    RelationshipPipeline,
)


@dataclass(frozen=True)
class BrainConfig:

    reader_registry: ReaderRegistry

    parser_registry: ParserRegistry

    chunker_registry: ChunkerRegistry

    embedding_pipeline: EmbeddingPipeline
    
    memory_pipeline: MemoryPipeline

    semantic_searcher: SemanticSearcher
    
    entity_pipeline: EntityPipeline
    
    relationship_pipeline: RelationshipPipeline
