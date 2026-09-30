import pytest

from brain.environment.docker.docker_compose import (
    DockerCompose,
)
from brain.environment.docker.docker_container import (
    DockerContainer,
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
from brain.perception.environment_observation_builder import (
    EnvironmentObservationBuilder,
)
from brain.perception.models.observation import (
    Observation,
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
from brain.workspace.models.signature import (
    Signature,
)
from brain.workspace.models.technology import (
    Technology,
)
from brain.workspace.models.workspace import (
    Workspace,
)


def create_environment(
    is_repository=True,
    branch_name="main",
    git_clean=True,
    docker_installed=True,
    docker_compose=True,
):
    workspace = Workspace(
        repository=Repository(
            files=10,
            directories=5,
            signatures={
                Signature(
                    value="pyproject.toml",
                    category="configuration",
                    path="pyproject.toml",
                ),
            },
        ),
        technologies={
            Technology(
                name="Python",
                category="language",
            ),
            Technology(
                name="Docker",
                category="container",
            ),
        },
        dependencies={
            Dependency(
                name="pytest",
            ),
            Dependency(
                name="requests",
            ),
        },
        architectures={
            Architecture(
                name="layered",
            ),
        },
    )

    return ProjectEnvironment(
        operating_system=OperatingSystem(
            name="Windows",
            version="11",
        ),
        git_repository=GitRepository(
            path=".",
            is_repository=is_repository,
        ),
        git_branch=GitBranch(
            name=branch_name,
        ),
        git_status=GitStatus(
            is_clean=git_clean,
        ),
        docker_environment=DockerEnvironment(
            info=DockerInfo(
                installed=docker_installed,
            ),
            containers=[
                DockerContainer(
                    container_id="container-1",
                    image="python:3.13",
                    name="test-container",
                    status="running",
                ),
            ],
            compose=DockerCompose(
                exists=docker_compose,
                path="docker-compose.yml",
            ),
        ),
        workspace=workspace,
    )


def test_build_creates_operating_system_observation():
    environment = create_environment()

    observations = (
        EnvironmentObservationBuilder()
        .build(environment)
    )

    assert Observation(
        source="environment",
        category="operating_system",
        subject="project",
        value="Windows",
    ) in observations


def test_git_repository_creates_observation():
    environment = create_environment(
        is_repository=True,
    )

    observations = (
        EnvironmentObservationBuilder()
        .build(environment)
    )

    assert Observation(
        source="environment",
        category="version_control",
        subject="project",
        value="git",
    ) in observations


def test_git_branch_creates_observation():
    environment = create_environment(
        branch_name="main",
    )

    observations = (
        EnvironmentObservationBuilder()
        .build(environment)
    )

    assert Observation(
        source="environment",
        category="branch",
        subject="repository",
        value="main",
    ) in observations


def test_git_clean_status_creates_clean_observation():
    environment = create_environment(
        git_clean=True,
    )

    observations = (
        EnvironmentObservationBuilder()
        .build(environment)
    )

    assert Observation(
        source="environment",
        category="git_status",
        subject="repository",
        value="clean",
    ) in observations


def test_git_dirty_status_creates_dirty_observation():
    environment = create_environment(
        git_clean=False,
    )

    observations = (
        EnvironmentObservationBuilder()
        .build(environment)
    )

    assert Observation(
        source="environment",
        category="git_status",
        subject="repository",
        value="dirty",
    ) in observations


def test_non_git_environment_has_no_git_observations():
    environment = create_environment(
        is_repository=False,
    )

    observations = (
        EnvironmentObservationBuilder()
        .build(environment)
    )

    assert not any(
        observation.category
        in {
            "version_control",
            "branch",
            "git_status",
        }
        for observation in observations
    )


def test_docker_creates_observation_when_installed():
    environment = create_environment(
        docker_installed=True,
    )

    observations = (
        EnvironmentObservationBuilder()
        .build(environment)
    )

    assert Observation(
        source="environment",
        category="container",
        subject="project",
        value="docker",
    ) in observations


def test_docker_compose_creates_observation_when_available():
    environment = create_environment(
        docker_installed=True,
        docker_compose=True,
    )

    observations = (
        EnvironmentObservationBuilder()
        .build(environment)
    )

    assert Observation(
        source="environment",
        category="container_orchestration",
        subject="project",
        value="docker_compose",
    ) in observations


def test_docker_compose_is_not_reported_when_unavailable():
    environment = create_environment(
        docker_installed=True,
        docker_compose=False,
    )

    observations = (
        EnvironmentObservationBuilder()
        .build(environment)
    )

    assert Observation(
        source="environment",
        category="container_orchestration",
        subject="project",
        value="docker_compose",
    ) not in observations


def test_docker_is_not_reported_when_not_installed():
    environment = create_environment(
        docker_installed=False,
        docker_compose=False,
    )

    observations = (
        EnvironmentObservationBuilder()
        .build(environment)
    )

    assert Observation(
        source="environment",
        category="container",
        subject="project",
        value="docker",
    ) not in observations


def test_workspace_technologies_become_observations():
    environment = create_environment()

    observations = (
        EnvironmentObservationBuilder()
        .build(environment)
    )

    for technology in environment.workspace.technologies:
        assert Observation(
            source="environment",
            category="technology",
            subject="workspace",
            value=technology.name,
        ) in observations


def test_workspace_dependencies_become_observations():
    environment = create_environment()

    observations = (
        EnvironmentObservationBuilder()
        .build(environment)
    )

    for dependency in environment.workspace.dependencies:
        assert Observation(
            source="environment",
            category="dependency",
            subject="workspace",
            value=dependency.name,
        ) in observations


def test_workspace_architectures_become_observations():
    environment = create_environment()

    observations = (
        EnvironmentObservationBuilder()
        .build(environment)
    )

    for architecture in environment.workspace.architectures:
        assert Observation(
            source="environment",
            category="architecture",
            subject="workspace",
            value=architecture.name,
        ) in observations


def test_build_returns_frozenset():
    environment = create_environment()

    observations = (
        EnvironmentObservationBuilder()
        .build(environment)
    )

    assert isinstance(
        observations,
        frozenset,
    )

    assert all(
        isinstance(
            observation,
            Observation,
        )
        for observation in observations
    )


def test_invalid_environment_raises_type_error():
    with pytest.raises(TypeError):
        EnvironmentObservationBuilder().build(
            "invalid",
        )