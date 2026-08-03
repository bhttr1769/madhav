from abc import ABC, abstractmethod


class BaseProvider(ABC):
    """
    Base interface for all AI providers.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """
        Returns the provider name.
        """
        pass

    @abstractmethod
    def is_available(self) -> bool:
        """
        Returns whether the provider is currently available.
        """
        pass