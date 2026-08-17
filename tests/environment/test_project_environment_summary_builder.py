from brain.environment.docker.docker_compose import (
    DockerCompose,
)

from brain.environment.docker.docker_environment import (
    DockerEnvironment,
)

from brain.environment.docker.docker_info import (
    DockerInfo,
)

from brain.environment.git.models.git_branch import (
    GitBranch,
)

from brain.environment.git.models.git_repository import (
    GitRepository,
)

from brain.environment.git.models.git_status import (
    GitStatus,
)

from brain.environment.models.operating_system import (
    OperatingSystem,
)

from brain.environment.models.project_environment import (
    ProjectEnvironment,
)

from brain.environment.project_environment_summary_builder import (
    ProjectEnvironmentSummaryBuilder,
)

from brain.workspace.models.architecture import (
    Architecture,
)

from brain.workspace.models.dependency import (
    Dependency,
)

from brain.workspace.models.repository import (
    Repository,
)

from brain.workspace.models.technology import (
    Technology,
)

from brain.workspace.models.workspace import (
    Workspace,
)


def test_project_environment_summary_builder():

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
                files=10,
                directories=2,
                signatures=set(),
            ),
            technologies={
                Technology(
                    name="Python",
                    category="language",
                ),
            },
            dependencies={
                Dependency(
                    name="pytest",
                ),
            },
            architectures={
                Architecture(
                    name="MVC",
                ),
            },
        ),
    )

    summary = (
        ProjectEnvironmentSummaryBuilder()
        .build(
            environment,
        )
    )

    assert (
        summary["operating_system"]
        == "Windows"
    )

    assert (
        summary["git_repository"]
        is True
    )

    assert (
        summary["git_branch"]
        == "main"
    )

    assert (
        summary["git_clean"]
        is True
    )

    assert (
        summary["docker_installed"]
        is True
    )

    assert (
        summary["workspace_files"]
        == 10
    )

    assert (
        "Python"
        in summary["technologies"]
    )