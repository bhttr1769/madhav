import pytest

from core.ai.config.model_config import ModelConfig
from core.ai.config.provider_config import ProviderConfig
from core.ai.config.runtime_config import RuntimeConfig
from core.ai.runtime.runtime_factory import RuntimeFactory


@pytest.fixture
def runtime_config() -> RuntimeConfig:

    return RuntimeConfig(
        provider=ProviderConfig(
            name="ollama",
            endpoint="http://localhost:11434",
        ),
        chat_model=ModelConfig(
            name="qwen2.5:1.5b",
        ),
        embedding_model=ModelConfig(
            name="nomic-embed-text",
        ),
    )


@pytest.fixture
def runtime(runtime_config):

    return RuntimeFactory.create(runtime_config)