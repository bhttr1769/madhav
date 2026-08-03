from abc import ABC, abstractmethod


class BaseEmbedding(ABC):
    """
    Base interface for all embedding providers.
    """

    @abstractmethod
    def embed(self, text: str) -> list[float]:
        """
        Convert text into a vector embedding.
        """
        raise NotImplementedError