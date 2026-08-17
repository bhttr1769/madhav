from dataclasses import dataclass

from brain.environment.models.operating_system import (
    OperatingSystem,
)

from brain.environment.git.models.git_repository import (
    GitRepository,
)

from brain.environment.git.models.git_branch import (
    GitBranch,
)

from brain.environment.git.models.git_status import (
    GitStatus,
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
class ProjectEnvironment:
    """
    Complete project environment.
    """

    operating_system: OperatingSystem

    git_repository: GitRepository

    git_branch: GitBranch

    git_status: GitStatus

    docker_environment: DockerEnvironment

    workspace: Workspace