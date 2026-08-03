from abc import abstractmethod

from core.ai.providers.base.base_provider import BaseProvider


class BaseEmbeddingProvider(BaseProvider):
    """
    Interface for providers that support embeddings.
    """

    @abstractmethod
    def embed(self, text: str) -> list[float]:
        """
        Generate an embedding vector for the given text.
        """
        pass