from pathlib import Path

from brain.environment.git.models.git_status import (
    GitStatus,
)


class GitStatusDetector:
    """
    Detects the state of a Git working tree.
    """

    def detect(
        self,
        path: str,
    ) -> GitStatus:

        git_directory = (
            Path(path)
            .joinpath(".git")
        )

        is_clean = (
            git_directory.exists()
        )

        return GitStatus(
            is_clean=is_clean,
        )