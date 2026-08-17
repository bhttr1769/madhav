from tests.environment.fake_terminal import (
    FakeTerminal,
)

from brain.environment.docker.docker_container_detector import (
    DockerContainerDetector,
)


def test_docker_container_detector():

    containers = (
        DockerContainerDetector(
            FakeTerminal(),
        )
    ).detect()

    assert (
        len(
            containers,
        )
        == 1
    )

    assert (
        containers[0].image
        == "postgres:16"
    )

    assert (
        containers[0].name
        == "postgres"
    )