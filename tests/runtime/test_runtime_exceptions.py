import pytest

from core.ai.runtime.provider_manager import ProviderManager

from core.ai.services.chat_service import ChatService

from core.ai.exceptions.provider_not_found import (
    ProviderNotFoundError,
)

from core.ai.exceptions.provider_unavailable import (
    ProviderUnavailableError,
)

from tests.runtime.fakes.unavailable_provider import (
    UnavailableProvider,
)


def test_chat_service_raises_provider_unavailable(
    runtime_config,
):

    manager = ProviderManager()

    manager.register(
        UnavailableProvider()
    )

    service = ChatService(
        config=runtime_config,
        provider_manager=manager,
    )

    with pytest.raises(
        ProviderUnavailableError
    ):
        service.chat("Hello")