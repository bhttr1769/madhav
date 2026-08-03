from brain.embedding.local_embedding import LocalEmbedding


class DummyLocalEmbedding(LocalEmbedding):

    def embed(self, text: str) -> list[float]:
        return [1.0, 2.0, 3.0]

    def is_available(self) -> bool:
        return True


def test_local_embedding():
    embedding = DummyLocalEmbedding()

    assert embedding.is_available()
    assert embedding.embed("hello") == [1.0, 2.0, 3.0]