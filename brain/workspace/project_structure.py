from pathlib import Path


class ProjectStructure:
    """
    Analyzes a project's directory structure.
    """

    def directories(
        self,
        files: list[Path],
    ) -> set[Path]:

        return {
            file.parent
            for file in files
        }