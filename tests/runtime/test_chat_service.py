from core.ai.runtime.provider_manager import ProviderManager
from core.ai.services.chat_service import ChatService
from tests.runtime.fakes.fake_provider import FakeProvider


def test_chat_service_returns_provider_response(runtime_config):

    manager = ProviderManager()

    manager.register(
        FakeProvider()
    )

    service = ChatService(
        config=runtime_config,
        provider_manager=manager,
    )

    response = service.chat("Hello")

    assert response == "Fake response"