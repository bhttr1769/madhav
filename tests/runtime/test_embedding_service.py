from core.ai.runtime.provider_manager import ProviderManager
from core.ai.services.embedding_service import EmbeddingService
from tests.runtime.fakes.fake_provider import FakeProvider


def test_embedding_service_returns_provider_embedding(runtime_config):

    manager = ProviderManager()

    manager.register(
        FakeProvider()
    )

    service = EmbeddingService(
        config=runtime_config,
        provider_manager=manager,
    )

    embedding = service.embed("Hello")

    assert embedding == [1.0, 2.0, 3.0]