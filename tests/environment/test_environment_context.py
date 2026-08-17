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


def test_environment_context():

    context = EnvironmentContext(
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

    assert context.git_repository.is_repository