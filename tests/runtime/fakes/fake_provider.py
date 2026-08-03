from core.ai.providers.base.base_chat_provider import BaseChatProvider
from core.ai.providers.base.base_embedding_provider import (
    BaseEmbeddingProvider,
)


class FakeProvider(
    BaseChatProvider,
    BaseEmbeddingProvider,
):
    """
    Fake provider used for runtime unit tests.
    """

    @property
    def name(self) -> str:
        return "ollama"

    def is_available(self) -> bool:
        return True

    def chat(self, prompt: str) -> str:
        return "Fake response"

    def embed(self, text: str) -> list[float]:
        return [1.0, 2.0, 3.0]