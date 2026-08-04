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
        )

        return BrainManager(config)