from core.ai.config.runtime_config import RuntimeConfig
from core.ai.runtime.provider_manager import ProviderManager


class EmbeddingService:
    """
    Provides embedding capabilities using the configured AI provider.
    """

    def __init__(
        self,
        config: RuntimeConfig,
        provider_manager: ProviderManager,
    ):
        self._config = config
        self._provider_manager = provider_manager

    def embed(self, text: str) -> list[float]:
        provider = self._provider_manager.get_embedding_provider(
            self._config.provider.name
        )

        return provider.embed(text)