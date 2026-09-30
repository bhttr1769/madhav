from dataclasses import fields, is_dataclass

from brain.environment.models.environment_context import (
    EnvironmentContext,
)
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


def create_context() -> EnvironmentContext:
    return EnvironmentContext(
        operating_system=OperatingSystem(
            name="Windows",
            version="11",
        ),
        git_repository=GitRepository(
            path=".",
            is_repository=True,
        ),
        docker_environment=None,
        workspace=None,
    )


def test_environment_context_is_a_frozen_dataclass():
    assert is_dataclass(EnvironmentContext)
    assert EnvironmentContext.__dataclass_params__.frozen is True


def test_environment_context_has_exact_field_order():
    assert tuple(
        field.name
        for field in fields(EnvironmentContext)
    ) == (
        "operating_system",
        "git_repository",
        "docker_environment",
        "workspace",
    )


def test_environment_context_stores_environment_components():
    context = create_context()

    assert isinstance(
        context.operating_system,
        OperatingSystem,
    )

    assert isinstance(
        context.git_repository,
        GitRepository,
    )

    assert context.docker_environment is None
    assert context.workspace is None


def test_environment_context_equality():
    first = create_context()
    second = create_context()

    assert first == second


def test_environment_context_is_immutable():
    context = create_context()

    try:
        context.workspace = None
    except AttributeError:
        pass
    else:
        raise AssertionError(
            "EnvironmentContext must be immutable"
        )