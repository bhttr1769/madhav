from pathlib import Path

from brain.environment.git.models.git_commit import (
    GitCommit,
)


class GitCommitDetector:
    """
    Detects the latest Git commit.
    """

    def detect(
        self,
        path: str,
    ) -> GitCommit:

        head_path = (
            Path(path)
            .joinpath(
                ".git",
                "HEAD",
            )
        )

        if not head_path.exists():

            return GitCommit(
                hash="",
            )

        return GitCommit(
            hash=(
                head_path
                .read_text()
                .strip()
            ),
        )