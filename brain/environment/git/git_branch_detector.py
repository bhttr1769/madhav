from pathlib import Path

from brain.environment.git.models.git_branch import (
    GitBranch,
)


class GitBranchDetector:
    """
    Detects the current Git branch.
    """

    def detect(
        self,
        path: str,
    ) -> GitBranch:

        head_path = (
            Path(path)
            .joinpath(
                ".git",
                "HEAD",
            )
        )

        if not head_path.exists():

            return GitBranch(
                name="",
            )

        head = (
            head_path
            .read_text()
            .strip()
        )

        return GitBranch(
            name=head.split("/")[-1],
        )