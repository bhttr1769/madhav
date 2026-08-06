from brain.config.embedding_config import EmbeddingConfig
from brain.factories.embedding_factory import EmbeddingFactory
from brain.config.brain_config import BrainConfig
from brain.manager import BrainManager
from brain.registry.chunker_registry import ChunkerRegistry
from brain.registry.parser_registry import ParserRegistry
from brain.registry.reader_registry import ReaderRegistry
from brain.embedding.embedding_pipeline import EmbeddingPipeline

from core.ai.config.model_config import ModelConfig
from core.ai.config.provider_config import ProviderConfig
from core.ai.config.runtime_config import RuntimeConfig
from core.ai.runtime.runtime_factory import RuntimeFactory

from brain.factories.search_factory import SearchFactory
from brain.factories.memory_factory import MemoryFactory

from brain.graph.extraction.rule_based_entity_extractor import (
    RuleBasedEntityExtractor,
)
from brain.graph.pipeline.entity_pipeline import EntityPipeline
from brain.graph.storage.graph_store import GraphStore

from brain.graph.extraction.rule_based_relationship_extractor import (
    RuleBasedRelationshipExtractor,
)
from brain.graph.pipeline.relationship_pipeline import (
    RelationshipPipeline,
)


class BrainFactory:
    """
    Responsible for creating fully configured BrainManager instances.
    """

    @staticmethod
    def create() -> BrainManager:

        runtime = RuntimeFactory.create(
            RuntimeConfig(
                provider=ProviderConfig(
                    name="ollama",
                    endpoint="http://localhost:11434",
                ),
                chat_model=ModelConfig(
                    name="qwen2.5:1.5b",
                ),
                embedding_model=ModelConfig(
                    name="nomic-embed-text",
                ),
            )
        )

        memory = MemoryFactory.create()

        search = SearchFactory.create(
            runtime=runtime,
            store=memory.store,
        )
        
        graph_store = GraphStore()
        entity_pipeline = EntityPipeline(
            extractor=RuleBasedEntityExtractor(),
            store=graph_store,
        )
        
        relationship_pipeline = RelationshipPipeline(
            extractor=RuleBasedRelationshipExtractor(),
            store=graph_store,
        )
        
        config = BrainConfig(
            reader_registry=ReaderRegistry(),
            parser_registry=ParserRegistry(),
            chunker_registry=ChunkerRegistry(),
            embedding_pipeline=EmbeddingPipeline(
                EmbeddingFactory.create(
                EmbeddingConfig()
                )
            ),
            memory_pipeline=memory.pipeline,
            semantic_searcher=search.semantic_searcher,
            entity_pipeline=entity_pipeline,
            relationship_pipeline=relationship_pipeline,
        )

        return BrainManager(config)