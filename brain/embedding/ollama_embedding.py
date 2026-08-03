from ollama import Client

from brain.config.embedding_config import EmbeddingConfig
from brain.embedding.local_embedding import LocalEmbedding


class OllamaEmbedding(LocalEmbedding):
    """
    Embedding provider backed by a local Ollama server.
    """

    def __init__(self, config: EmbeddingConfig):
        self._config = config
        self._client = Client(host=config.host)

    def embed(self, text: str) -> list[float]:
        response = self._client.embed(
            model=self._config.model_name,
            input=text,
        )

        return response["embeddings"][0]

    def is_available(self) -> bool:
        try:
            self._client.list()
            return True
        except Exception:
            return False