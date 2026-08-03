from abc import abstractmethod

from core.ai.providers.base.base_provider import BaseProvider


class BaseChatProvider(BaseProvider):
    """
    Interface for providers that support chat.
    """

    @abstractmethod
    def chat(self, prompt: str) -> str:
        """
        Generate a response for the given prompt.
        """
        pass