from brain.environment.models.project_environment import (
    ProjectEnvironment,
)


class ProjectEnvironmentSummaryBuilder:
    """
    Builds a serializable project environment summary.
    """

    def build(
        self,
        environment: ProjectEnvironment,
    ) -> dict:

        return {
            "operating_system": (
                environment.operating_system.name
            ),
            "git_repository": (
                environment.git_repository.is_repository
            ),
            "git_branch": (
                environment.git_branch.name
            ),
            "git_clean": (
                environment.git_status.is_clean
            ),
            "docker_installed": (
                environment.docker_environment
                .info
                .installed
            ),
            "docker_compose": (
                environment.docker_environment
                .compose
                .exists
            ),
            "workspace_files": (
                environment.workspace
                .repository
                .files
            ),
            "workspace_directories": (
                environment.workspace
                .repository
                .directories
            ),
            "technologies": {
                technology.name
                for technology in (
                    environment.workspace
                    .technologies
                )
            },
            "dependencies": {
                dependency.name
                for dependency in (
                    environment.workspace
                    .dependencies
                )
            },
            "architectures": {
                architecture.name
                for architecture in (
                    environment.workspace
                    .architectures
                )
            },
        }