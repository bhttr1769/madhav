from brain.environment.models.project_environment import (
    ProjectEnvironment,
)

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

from brain.environment.docker.docker_info import (
    DockerInfo,
)

from brain.environment.docker.docker_compose import (
    DockerCompose,
)

from brain.workspace.models.repository import (
    Repository,
)

from brain.workspace.models.workspace import (
    Workspace,
)


def test_project_environment():

    environment = ProjectEnvironment(
        operating_system=OperatingSystem(
            name="Windows",
            version="11",
        ),
        git_repository=GitRepository(
            path=".",
            is_repository=True,
        ),
        git_branch=GitBranch(
            name="main",
        ),
        git_status=GitStatus(
            is_clean=True,
        ),
        docker_environment=DockerEnvironment(
            info=DockerInfo(
                installed=True,
            ),
            containers=[],
            compose=DockerCompose(
                exists=False,
                path="",
            ),
        ),
        workspace=Workspace(
            repository=Repository(
                files=0,
                directories=0,
                signatures=set(),
            ),
            technologies=set(),
            dependencies=set(),
            architectures=set(),
        ),
    )

    assert (
        environment.operating_system.name
        == "Windows"
    )

    assert (
        environment.git_repository.is_repository
        is True
    )

    assert (
        environment.git_status.is_clean
        is True
    )