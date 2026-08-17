from dataclasses import dataclass

from brain.environment.models.operating_system import (
    OperatingSystem,
)

from brain.environment.git.models.git_repository import (
    GitRepository,
)

from brain.environment.docker.docker_environment import (
    DockerEnvironment,
)

from brain.workspace.models.workspace import (
    Workspace,
)


@dataclass(
    frozen=True,
)
class EnvironmentContext:

    operating_system: OperatingSystem

    git_repository: GitRepository

    docker_environment: DockerEnvironment

    workspace: Workspace