from dataclasses import dataclass

from brain.config.base_config import BaseConfig


@dataclass(frozen=True)
class EmbeddingConfig(BaseConfig):
    """
    Configuration for embedding providers.
    """

    provider: str = "ollama"
    model_name: str = "nomic-embed-text"
    host: str = "http://localhost:11434"