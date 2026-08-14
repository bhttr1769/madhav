from pathlib import Path

from brain.models.document import Document
from brain.filesystem.folder_learner import (
    FolderLearner,
)


class KnowledgeBaseBuilder:
    """
    Builds a knowledge base from a directory.
    """

    def __init__(
        self,
        brain,
    ):
        self._learner = FolderLearner(
            brain,
        )

    def build(
        self,
        directory: str | Path,
    ) -> list[Document]:

        return self._learner.learn(
            directory,
        )