from brain.config.embedding_config import EmbeddingConfig
from brain.embedding.ollama_embedding import OllamaEmbedding


def test_ollama_embedding_creation():
    config = EmbeddingConfig()

    embedding = OllamaEmbedding(config)

    assert embedding is not None