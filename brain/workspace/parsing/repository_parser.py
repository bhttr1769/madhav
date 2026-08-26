from pathlib import Path

from brain.workspace.models.directory import (
    Directory,
)

from brain.workspace.models.file import (
    File,
)

from brain.workspace.models.parsed_repository import (
    ParsedRepository,
)

from brain.workspace.extraction.signature_extractor import (
    SignatureExtractor,
)

from brain.workspace.parsing.file_classifier import (
    FileClassifier,
)

from brain.workspace.discovery.workspace_scanner import (
    WorkspaceScanner,
)


class RepositoryParser:
    """
    Parses a workspace into structured repository knowledge.
    """

    def __init__(
        self,
        classifier: FileClassifier | None = None,
        signature_extractor: SignatureExtractor | None = None,
    ):

        self._classifier = (
            classifier
            if classifier is not None
            else FileClassifier()
        )

        self._signature_extractor = (
            signature_extractor
            if signature_extractor is not None
            else SignatureExtractor()
        )

        self._scanner = WorkspaceScanner()

    def parse(
        self,
        workspace: str | Path,
    ) -> ParsedRepository:

        root = Path(
            workspace
        ).resolve()

        files = set()

        directories = set()

        paths = [
            path
            for path in root.rglob("*")
        ] 

        for path in paths:

            if path.is_dir():

                directories.add(
                    Directory(
                        name=path.name,
                        path=str(path),
                    )
                )

                continue

            if not path.is_file():
                continue

            files.add(
                File(
                    name=path.name,
                    path=str(path),
                    extension=path.suffix.lower(),
                    category=(
                        self._classifier.classify(
                            path,
                        ) 
                    ),
                    metadata=frozenset({
                        (
                            "relative_path",
                            str(
                                path.relative_to(
                                    root,
                                )
                            ),
                        ),
                    }),
                )
            )

        file_paths = [
            Path(file.path)
            for file in files
        ]

        signatures = (
            self._signature_extractor.extract(
                file_paths,
            )
        )

        return ParsedRepository(
            root=str(root),
            files=frozenset(files),
            directories=frozenset(
                directories
            ),
            signatures=frozenset(
                signatures
            ),
        )