from core.ai.config.runtime_config import RuntimeConfig
from core.ai.providers.ollama.ollama_provider import OllamaProvider
from core.ai.runtime.ai_runtime import AIRuntime
from core.ai.runtime.provider_manager import ProviderManager
from core.ai.services.chat_service import ChatService
from core.ai.services.embedding_service import EmbeddingService


class RuntimeFactory:
    """
    Factory responsible for building the AI Runtime.
    """

    @staticmethod
    def create(config: RuntimeConfig) -> AIRuntime:

        provider_manager = ProviderManager()

        provider_manager.register(
            OllamaProvider(config)
        )

        chat_service = ChatService(
            config=config,
            provider_manager=provider_manager,
        )

        embedding_service = EmbeddingService(
            config=config,
            provider_manager=provider_manager,
        )

        return AIRuntime(
            config=config,
            provider_manager=provider_manager,
            chat=chat_service,
            embedding=embedding_service,
        )