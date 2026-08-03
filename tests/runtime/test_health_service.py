from core.ai.runtime.provider_manager import ProviderManager
from core.ai.services.health_service import HealthService
from tests.runtime.fakes.fake_provider import FakeProvider


def test_health_service_returns_runtime_status(runtime_config):

    manager = ProviderManager()

    manager.register(
        FakeProvider()
    )

    service = HealthService(
        config=runtime_config,
        provider_manager=manager,
    )

    health = service.status()

    assert health.status == "healthy"

    assert health.provider == "ollama"

    assert health.provider_available is True

    assert health.chat_model == "qwen2.5:1.5b"

    assert health.embedding_model == "nomic-embed-text"

    assert health.chat_available is True

    assert health.embedding_available is True