from brain.environment.detectors.os_detector import (
    OSDetector,
)

from brain.environment.docker.docker_environment_detector import (
    DockerEnvironmentDetector,
)

from brain.environment.git.git_service import (
    GitService,
)

from brain.environment.models.project_environment import (
    ProjectEnvironment,
)

from brain.workspace.workspace_manager import (
    WorkspaceManager,
)


class ProjectEnvironmentScanner:
    """
    Scans the complete project environment.
    """

    def __init__(
        self,
        workspace_manager: WorkspaceManager,
        docker_environment_detector: (
            DockerEnvironmentDetector
        ),
    ):

        self._os_detector = (
            OSDetector()
        )

        self._git_service = (
            GitService()
        )

        self._docker_detector = (
            docker_environment_detector
        )

        self._workspace_manager = (
            workspace_manager
        )

    def scan(
        self,
        path=".",
    ) -> ProjectEnvironment:

        return ProjectEnvironment(
            operating_system=(
                self._os_detector.detect()
            ),
            git_repository=(
                self._git_service.repository(
                    path,
                )
            ),
            git_branch=(
                self._git_service.branch(
                    path,
                )
            ),
            git_status=(
                self._git_service.status(
                    path,
                )
            ),
            docker_environment=(
                self._docker_detector.detect(
                    path,
                )
            ),
            workspace=(
                self._workspace_manager.learn(
                    path,
                )
            ),
        )