from pathlib import Path

from brain.workspace.models.repository import (
    Repository,
)

from brain.workspace.extraction.signature_extractor import (
    SignatureExtractor,
)


class RepositoryFingerprint:
    """
    Builds a repository fingerprint.
    """

    def __init__(self):

        self._extractor = (
            SignatureExtractor()
        )

    def build(
        self,
        files: list[Path],
    ) -> Repository:

        signatures = (
            self._extractor.extract(
                files,
            )
        )

        directories = set()

        for file in files:

            directories.add(
                file.parent
            )

        return Repository(
            files=len(files),
            directories=len(
                directories
            ),
            signatures=signatures,
        )