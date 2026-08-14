from pathlib import Path

from brain.workspace.project_analyzer import (
    ProjectAnalyzer,
)
from brain.workspace.project_structure import (
    ProjectStructure,
)
from brain.workspace.technology_detector import (
    TechnologyDetector,
)
from brain.workspace.repository_analyzer import (
    RepositoryAnalyzer,
)


class ProjectSummary:
    """
    Builds a project summary.
    """

    def __init__(self):

        self._analyzer = (
            ProjectAnalyzer()
        )

        self._detector = (
            TechnologyDetector()
        )

        self._structure = (
            ProjectStructure()
        )

        self._repository = (
            RepositoryAnalyzer()
        )

    def build(
        self,
        files: list[Path],
    ) -> dict:

        return {
            "file_count":
            self._analyzer.file_count(
                files,
            ),

            "technologies":
            self._detector.detect(
                files,
            ),

            "directories":
            self._structure.directories(
                files,
            ),

            "repository":
            self._repository.analyze(
                files,
            ),
        }