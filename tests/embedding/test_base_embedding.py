import pytest

from brain.embedding.base_embedding import BaseEmbedding


class DummyEmbedding(BaseEmbedding):
    def embed(self, text: str) -> list[float]:
        return [0.1, 0.2, 0.3]


def test_dummy_embedding():
    embedding = DummyEmbedding()

    vector = embedding.embed("Hello")

    assert vector == [0.1, 0.2, 0.3]