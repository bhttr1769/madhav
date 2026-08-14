from pathlib import Path

from brain.workspace.discovery.workspace_scanner import (
    WorkspaceScanner,
)

from brain.workspace.repository_fingerprint import (
    RepositoryFingerprint,
)

from brain.workspace.models.workspace import (
    Workspace,
)


class WorkspaceLearner:
    """
    Learns an entire workspace.
    """

    def __init__(
        self,
        language_detector,
        dependency_detector,
        architecture_detector,
    ):

        self._scanner = (
            WorkspaceScanner()
        )

        self._repository = (
            RepositoryFingerprint()
        )

        self._language_detector = (
            language_detector
        )

        self._dependency_detector = (
            dependency_detector
        )

        self._architecture_detector = (
            architecture_detector
        )

    def learn(
        self,
        workspace: str | Path,
    ) -> Workspace:

        files = self._scanner.scan(
            workspace,
        )

        repository = (
            self._repository.build(
                files,
            )
        )

        signatures = (
            repository.signatures
        )

        return Workspace(
            repository=repository,
            technologies=(
                self._language_detector.detect(
                    signatures,
                )
            ),
            dependencies=(
                self._dependency_detector.detect(
                    signatures,
                )
            ),
            architectures=(
                self._architecture_detector.detect(
                    signatures,
                )
            ),
        )