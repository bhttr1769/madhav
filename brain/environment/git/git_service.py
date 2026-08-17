from brain.environment.git.git_branch_detector import (
    GitBranchDetector,
)

from brain.environment.git.git_commit_detector import (
    GitCommitDetector,
)

from brain.environment.git.git_detector import (
    GitDetector,
)

from brain.environment.git.git_status_detector import (
    GitStatusDetector,
)

class GitService:
    """
    Provides Git environment information.
    """

    def __init__(
        self,
    ):

        self._repository_detector = (
            GitDetector()
        )

        self._branch_detector = (
            GitBranchDetector()
        )

        self._status_detector = (
            GitStatusDetector()
        )

        self._commit_detector = (
            GitCommitDetector()
        )

    def repository(
        self,
        path,
    ):

        return (
            self._repository_detector.detect(
                path,
            )
        )

    def branch(
        self,
        path,
    ):

        try:

            return (
                self._branch_detector.detect(
                    path,
                )
            )

        except Exception:

            return self._branch_detector.detect(
                "",
            )

    def status(
        self,
        path,
    ):

        return (
            self._status_detector.detect(
                path,
            )
        )

    def commit(
        self,
        path,
    ):

        try:

            return (
                self._commit_detector.detect(
                    path,
                )
            )

        except Exception:

            return self._commit_detector.detect(
                "",
            )