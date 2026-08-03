from core.ai.config.runtime_config import RuntimeConfig
from core.ai.models.health_status import HealthStatus
from core.ai.runtime.provider_manager import ProviderManager


class HealthService:
    """
    Provides health information about the AI Runtime.
    """

    def __init__(
        self,
        config: RuntimeConfig,
        provider_manager: ProviderManager,
    ):
        self._config = config
        self._provider_manager = provider_manager

    def status(self) -> HealthStatus:

        provider = self._provider_manager.get(
            self._config.provider.name
        )

        available = provider.is_available()

        return HealthStatus(
            status="healthy" if available else "unhealthy",
            provider=provider.name,
            provider_available=available,
            chat_model=self._config.chat_model.name,
            embedding_model=self._config.embedding_model.name,
            chat_available=available,
            embedding_available=available,
        )