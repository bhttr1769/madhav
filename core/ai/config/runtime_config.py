from dataclasses import dataclass

from core.ai.config.model_config import ModelConfig
from core.ai.config.provider_config import ProviderConfig


@dataclass(frozen=True)
class RuntimeConfig:
    """
    Global AI Runtime configuration.
    """

    provider: ProviderConfig
    chat_model: ModelConfig
    embedding_model: ModelConfig
    enable_streaming: bool = True