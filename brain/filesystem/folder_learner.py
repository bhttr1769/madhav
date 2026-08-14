from pathlib import Path

from brain.filesystem.recursive_directory_scanner import (
    RecursiveDirectoryScanner,
)
from brain.filesystem.supported_file_filter import (
    SupportedFileFilter,
)


class FolderLearner:
    """
    Learns all documents inside a folder.
    """

    def __init__(
        self,
        brain,
    ):
        self._brain = brain

        self._scanner = (
            RecursiveDirectoryScanner()
        )

        self._filter = (
            SupportedFileFilter()
        )

    def learn(
        self,
        directory: str | Path,
    ):

        files = self._scanner.scan(
            directory,
        )

        files = self._filter.filter(
            files,
        )

        learned_documents = []

        for file in files:

            document = self._brain.learn(
                file,
            )

            learned_documents.append(
                document
            )

        return learned_documents