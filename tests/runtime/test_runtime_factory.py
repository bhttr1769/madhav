from core.ai.runtime.ai_runtime import AIRuntime
from core.ai.services.chat_service import ChatService
from core.ai.services.embedding_service import EmbeddingService
from core.ai.services.health_service import HealthService


def test_runtime_factory_creates_runtime(runtime):

    assert isinstance(runtime, AIRuntime)


def test_runtime_contains_chat_service(runtime):

    assert isinstance(runtime.chat, ChatService)


def test_runtime_contains_embedding_service(runtime):

    assert isinstance(runtime.embedding, EmbeddingService)


def test_runtime_contains_health_service(runtime):

    assert isinstance(runtime.health, HealthService)