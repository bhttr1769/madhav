from brain.filesystem.folder_learner import (
    FolderLearner,
)


class FakeDocument:

    pass


class FakeBrain:

    def __init__(self):

        self.learned = []

    def learn(
        self,
        file_path,
    ):

        document = FakeDocument()

        self.learned.append(
            document
        )

        return document


def test_folder_learner(
    tmp_path,
):

    folder = tmp_path / "notes"

    folder.mkdir()

    file1 = folder / "java.txt"

    file2 = folder / "spring.txt"

    file1.write_text(
        "java"
    )

    file2.write_text(
        "spring"
    )

    brain = FakeBrain()

    learner = FolderLearner(
        brain,
    )

    documents = learner.learn(
    folder,
    )

    assert len(documents) == 2

    assert len(brain.learned) == 2