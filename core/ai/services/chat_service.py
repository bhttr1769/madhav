from core.ai.config.runtime_config import RuntimeConfig
from core.ai.runtime.provider_manager import ProviderManager


class ChatService:
    """
    Provides chat capabilities using the configured AI provider.
    """

    def __init__(
        self,
        config: RuntimeConfig,
        provider_manager: ProviderManager,
    ):
        self._config = config
        self._provider_manager = provider_manager

    def chat(self, prompt: str) -> str:
        provider = self._provider_manager.get_chat_provider(
            self._config.provider.name
        )

        return provider.chat(prompt)