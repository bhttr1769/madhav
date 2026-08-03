import pytest

from core.ai.runtime.provider_manager import ProviderManager
from core.ai.providers.ollama.ollama_provider import OllamaProvider
from core.ai.exceptions.provider_not_found import ProviderNotFoundError


def test_provider_can_be_registered(runtime_config):

    manager = ProviderManager()

    provider = OllamaProvider(runtime_config)

    manager.register(provider)

    assert manager.is_registered("ollama")


def test_registered_provider_can_be_retrieved(runtime_config):

    manager = ProviderManager()

    provider = OllamaProvider(runtime_config)

    manager.register(provider)

    assert manager.get("ollama") is provider


def test_unknown_provider_raises_exception():

    manager = ProviderManager()

    with pytest.raises(ProviderNotFoundError):

        manager.get("unknown")


def test_provider_list(runtime_config):

    manager = ProviderManager()

    manager.register(
        OllamaProvider(runtime_config)
    )

    providers = manager.providers()

    assert "ollama" in providers