from brain.environment.docker.docker_detector import (
    DockerDetector,
)


def test_docker_detector():

    info = (
        DockerDetector()
    ).detect()

    assert (
        isinstance(
            info.installed,
            bool,
        )
    )