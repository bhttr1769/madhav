from core.ai.exceptions.provider_not_found import ProviderNotFoundError
from core.ai.providers.base.base_provider import BaseProvider
from core.ai.providers.base.base_chat_provider import BaseChatProvider
from core.ai.providers.base.base_embedding_provider import BaseEmbeddingProvider


class ProviderManager:
    """
    Registers and manages AI providers.
    """

    def __init__(self):
        self._providers: dict[str, BaseProvider] = {}

    def register(self, provider: BaseProvider) -> None:
        """
        Register a provider.
        """
        self._providers[provider.name] = provider

    def get(self, name: str) -> BaseProvider:
        """
        Retrieve a provider by name.
        """
        provider = self._providers.get(name)

        if provider is None:
            raise ProviderNotFoundError(name)

        return provider
    def get_chat_provider(self, name: str) -> BaseChatProvider:
        """
        Retrieve a chat-capable provider.
        """
        provider = self.get(name)

        if not isinstance(provider, BaseChatProvider):
            raise TypeError(
                f"Provider '{name}' does not support chat."
            )

        return provider


    def get_embedding_provider(self, name: str) -> BaseEmbeddingProvider:
        """
        Retrieve an embedding-capable provider.
        """
        provider = self.get(name)

        if not isinstance(provider, BaseEmbeddingProvider):
            raise TypeError(
                f"Provider '{name}' does not support embeddings."
            )

        return provider

    def is_registered(self, name: str) -> bool:
        """
        Check whether a provider is registered.
        """
        return name in self._providers

    def providers(self) -> list[str]:
        """
        Return the names of all registered providers.
        """
        return list(self._providers.keys())