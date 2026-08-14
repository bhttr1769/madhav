from pathlib import Path


class ProjectAnalyzer:
    """
    Analyzes a project's files.
    """

    def file_count(
        self,
        files: list[Path],
    ) -> int:

        return len(files)