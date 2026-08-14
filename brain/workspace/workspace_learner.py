from pathlib import Path

from brain.filesystem.recursive_directory_scanner import (
    RecursiveDirectoryScanner,
)
from brain.workspace.project_summary import (
    ProjectSummary,
)


class WorkspaceLearner:
    """
    Learns an entire workspace.
    """

    def __init__(
        self,
        brain,
    ):

        self._brain = brain

        self._scanner = (
            RecursiveDirectoryScanner()
        )

        self._summary = (
            ProjectSummary()
        )

    def learn(
        self,
        folder: str | Path,
    ) -> dict:

        files = self._scanner.scan(
            folder,
        )

        for file in files:

            self._brain.learn(
                file,
            )

        return self._summary.build(
            files,
        )