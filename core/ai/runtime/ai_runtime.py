from core.ai.config.runtime_config import RuntimeConfig
from core.ai.runtime.provider_manager import ProviderManager
from core.ai.services.chat_service import ChatService
from core.ai.services.embedding_service import EmbeddingService
from core.ai.services.health_service import HealthService


class AIRuntime:
    """
    Entry point for all AI capabilities.
    """

    def __init__(
        self,
        config: RuntimeConfig,
        provider_manager: ProviderManager,
        chat: ChatService,
        embedding: EmbeddingService,
        health: HealthService,
    ):
        self._config = config
        self._provider_manager = provider_manager

        self.chat = chat
        self.embedding = embedding
        self.health = health

    @property
    def config(self) -> RuntimeConfig:
        return self._config

    @property
    def provider_manager(self) -> ProviderManager:
        return self._provider_manager