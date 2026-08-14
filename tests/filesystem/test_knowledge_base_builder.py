from brain.filesystem.knowledge_base_builder import (
    KnowledgeBaseBuilder,
)


class FakeDocument:

    pass


class FakeBrain:

    def learn(
        self,
        file_path,
    ):

        return FakeDocument()


def test_knowledge_base_builder(
    tmp_path,
):

    folder = tmp_path / "documents"

    folder.mkdir()

    (folder / "java.txt").write_text(
        "java"
    )

    builder = KnowledgeBaseBuilder(
        FakeBrain(),
    )

    documents = builder.build(
        folder,
    )

    assert len(documents) == 1