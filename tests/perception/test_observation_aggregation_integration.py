from brain.perception.environment_observation_builder import (
    EnvironmentObservationBuilder,
)
from brain.perception.models.observation import (
    Observation,
)
from brain.perception.perception_aggregator import (
    PerceptionAggregator,
)


def test_environment_observations_can_be_aggregated():
    environment_observations = (
        EnvironmentObservationBuilder()
        .build(
            create_environment(),
        )
    )

    additional_observation = Observation(
        source="code",
        category="technology",
        subject="module",
        value="Python",
    )

    observations = list(
        environment_observations
    )

    observations.append(
        additional_observation,
    )

    aggregated = (
        PerceptionAggregator()
        .aggregate(observations)
    )

    assert isinstance(
        aggregated,
        frozenset,
    )

    assert environment_observations.issubset(
        aggregated,
    )

    assert additional_observation in aggregated


def test_aggregator_removes_exact_duplicate_observations():
    observation = Observation(
        source="environment",
        category="technology",
        subject="workspace",
        value="Python",
    )

    aggregated = (
        PerceptionAggregator()
        .aggregate(
            [
                observation,
                observation,
            ]
        )
    )

    assert aggregated == frozenset(
        {
            observation,
        }
    )


def test_aggregator_preserves_distinct_observations():
    first = Observation(
        source="environment",
        category="technology",
        subject="workspace",
        value="Python",
    )

    second = Observation(
        source="code",
        category="technology",
        subject="module",
        value="Python",
    )

    aggregated = (
        PerceptionAggregator()
        .aggregate(
            [
                first,
                second,
            ]
        )
    )

    assert aggregated == frozenset(
        {
            first,
            second,
        }
    )


def create_environment():
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
        },
        dependencies={
            Dependency(
                name="pytest",
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
            containers=[],
            compose=DockerCompose(
                exists=True,
                path="docker-compose.yml",
            ),
        ),
        workspace=workspace,
    )