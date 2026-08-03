from brain.config.embedding_config import EmbeddingConfig
from brain.embedding.base_embedding import BaseEmbedding
from brain.embedding.ollama_embedding import OllamaEmbedding


class EmbeddingFactory:
    """
    Responsible for creating embedding providers.
    """

    @staticmethod
    def create(config: EmbeddingConfig) -> BaseEmbedding:

        if config.provider == "ollama":
            return OllamaEmbedding(config)

        raise ValueError(
            f"Unsupported embedding provider: {config.provider}"
        )