from pathlib import Path

from brain.environment.git.models.git_repository import (
    GitRepository,
)


class GitDetector:
    """
    Detects Git repositories.
    """

    def detect(
        self,
        path: str,
    ) -> GitRepository:

        repository_path = Path(path)

        return GitRepository(
            path=str(repository_path),
            is_repository=repository_path
            .joinpath(".git")
            .exists(),
        )