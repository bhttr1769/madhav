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


def create_environment():
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
            containers=[
                DockerContainer(
                    container_id="container-1",
                    image="python:3.13",
                    name="test-container",
                    status="running",
                ),
            ],
            compose=DockerCompose(
                exists=True,
                path="docker-compose.yml",
            ),
        ),
        workspace=workspace,
    )


def test_workspace_technologies_flow_into_observations():
    environment = create_environment()

    observations = (
        EnvironmentObservationBuilder()
        .build(environment)
    )

    assert Observation(
        source="environment",
        category="technology",
        subject="workspace",
        value="Python",
    ) in observations

    assert Observation(
        source="environment",
        category="technology",
        subject="workspace",
        value="Docker",
    ) in observations


def test_workspace_dependencies_flow_into_observations():
    environment = create_environment()

    observations = (
        EnvironmentObservationBuilder()
        .build(environment)
    )

    assert Observation(
        source="environment",
        category="dependency",
        subject="workspace",
        value="pytest",
    ) in observations

    assert Observation(
        source="environment",
        category="dependency",
        subject="workspace",
        value="requests",
    ) in observations


def test_workspace_architectures_flow_into_observations():
    environment = create_environment()

    observations = (
        EnvironmentObservationBuilder()
        .build(environment)
    )

    assert Observation(
        source="environment",
        category="architecture",
        subject="workspace",
        value="layered",
    ) in observations


def test_workspace_observations_preserve_workspace_subject():
    environment = create_environment()

    observations = (
        EnvironmentObservationBuilder()
        .build(environment)
    )

    workspace_observations = {
        observation
        for observation in observations
        if observation.category
        in {
            "technology",
            "dependency",
            "architecture",
        }
    }

    assert workspace_observations

    assert all(
        observation.subject == "workspace"
        for observation in workspace_observations
    )


def test_workspace_observation_values_are_derived_from_workspace():
    environment = create_environment()

    observations = (
        EnvironmentObservationBuilder()
        .build(environment)
    )

    expected = {
        Observation(
            source="environment",
            category="technology",
            subject="workspace",
            value=technology.name,
        )
        for technology in environment.workspace.technologies
    }

    expected |= {
        Observation(
            source="environment",
            category="dependency",
            subject="workspace",
            value=dependency.name,
        )
        for dependency in environment.workspace.dependencies
    }

    expected |= {
        Observation(
            source="environment",
            category="architecture",
            subject="workspace",
            value=architecture.name,
        )
        for architecture in environment.workspace.architectures
    }

    assert expected.issubset(observations)