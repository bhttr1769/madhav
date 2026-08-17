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

from brain.environment.project_environment_graph_builder import (
    ProjectEnvironmentGraphBuilder,
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


def test_project_environment_graph_builder():

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

    graph = (
        ProjectEnvironmentGraphBuilder()
        .build(
            environment,
        )
    )

    assert (
        graph.get_node(
            "project",
        )
        is not None
    )

    assert (
        graph.get_node(
            "Windows",
        )
        is not None
    )

    assert (
        graph.get_node(
            "git",
        )
        is not None
    )

    assert (
        graph.get_node(
            "docker",
        )
        is not None
    )

    assert (
        graph.get_node(
            "Python",
        )
        is not None
    )