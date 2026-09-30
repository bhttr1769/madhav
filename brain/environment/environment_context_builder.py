from brain.environment.models.environment_context import (
    EnvironmentContext,
)

from brain.environment.project_environment_scanner import (
    ProjectEnvironmentScanner,
)


class EnvironmentContextBuilder:

    def __init__(
        self,
        scanner: ProjectEnvironmentScanner,
    ):

        if not isinstance(
            scanner,
            ProjectEnvironmentScanner,
        ):
            raise TypeError(
                "scanner must be a ProjectEnvironmentScanner"
            )

        self._scanner = scanner

    def build(
        self,
        workspace_path=".",
    ) -> EnvironmentContext:

        environment = self._scanner.scan(
            workspace_path,
        )

        return EnvironmentContext(
            operating_system=(
                environment.operating_system
            ),
            git_repository=(
                environment.git_repository
            ),
            docker_environment=(
                environment.docker_environment
            ),
            workspace=(
                environment.workspace
            ),
        )