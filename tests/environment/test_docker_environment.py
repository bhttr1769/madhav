from brain.environment.docker.docker_compose import (
    DockerCompose,
)

from brain.environment.docker.docker_environment_detector import (
    DockerEnvironmentDetector,
)

from brain.environment.docker.docker_info import (
    DockerInfo,
)


class FakeDockerDetector:

    def detect(
        self,
    ):

        return DockerInfo(
            installed=True,
        )


class FakeContainerDetector:

    def detect(
        self,
    ):

        return []


class FakeComposeDetector:

    def detect(
        self,
        path=".",
    ):

        return DockerCompose(
            exists=True,
            path="docker-compose.yml",
        )


def test_docker_environment_detector():

    environment = (
        DockerEnvironmentDetector(
            FakeDockerDetector(),
            FakeContainerDetector(),
            FakeComposeDetector(),
        )
    ).detect()

    assert (
        environment.info.installed
        is True
    )

    assert (
        environment.compose.exists
        is True
    )

    assert (
        len(
            environment.containers,
        )
        == 0
    )