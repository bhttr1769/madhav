from core.ai.providers.base.base_chat_provider import BaseChatProvider
from core.ai.providers.base.base_embedding_provider import (
    BaseEmbeddingProvider,
)
from core.ai.exceptions.provider_unavailable import (
    ProviderUnavailableError,
)


class UnavailableProvider(
    BaseChatProvider,
    BaseEmbeddingProvider,
):

    @property
    def name(self):
        return "ollama"

    def is_available(self):
        return False

    def chat(self, prompt: str):

        raise ProviderUnavailableError(
            self.name
        )

    def embed(self, text: str):

        raise ProviderUnavailableError(
            self.name
        )