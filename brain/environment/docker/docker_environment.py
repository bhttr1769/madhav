from dataclasses import dataclass

from brain.environment.docker.docker_compose import (
    DockerCompose,
)

from brain.environment.docker.docker_container import (
    DockerContainer,
)

from brain.environment.docker.docker_info import (
    DockerInfo,
)


@dataclass(
    frozen=True,
)
class DockerEnvironment:

    info: DockerInfo

    containers: list[DockerContainer]

    compose: DockerCompose