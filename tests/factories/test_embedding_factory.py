import pytest

from brain.config.embedding_config import EmbeddingConfig
from brain.embedding.ollama_embedding import OllamaEmbedding
from brain.factories.embedding_factory import EmbeddingFactory


def test_create_ollama_embedding():
    config = EmbeddingConfig()

    embedding = EmbeddingFactory.create(config)

    assert isinstance(embedding, OllamaEmbedding)


def test_unknown_provider():
    config = EmbeddingConfig(
        provider="unknown"
    )

    with pytest.raises(ValueError):
        EmbeddingFactory.create(config)