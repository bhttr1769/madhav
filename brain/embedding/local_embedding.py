from abc import abstractmethod

from brain.embedding.base_embedding import BaseEmbedding


class LocalEmbedding(BaseEmbedding):
    """
    Base class for all locally hosted embedding providers.
    """

    @abstractmethod
    def is_available(self) -> bool:
        """
        Returns True if the embedding backend is available.
        """
        raise NotImplementedError