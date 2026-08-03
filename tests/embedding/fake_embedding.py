from brain.embedding.base_embedding import BaseEmbedding


class FakeEmbedding(BaseEmbedding):
    """
    Fake embedding provider used for unit tests.
    """

    def embed(self, text: str) -> list[float]:
        return [0.1, 0.2, 0.3]