from brain.environment.docker.docker_environment import (
    DockerEnvironment,
)


class DockerEnvironmentDetector:

    def __init__(
        self,
        docker_detector,
        container_detector,
        compose_detector,
    ):

        self._docker_detector = (
            docker_detector
        )

        self._container_detector = (
            container_detector
        )

        self._compose_detector = (
            compose_detector
        )

    def detect(
        self,
        path=".",
    ) -> DockerEnvironment:

        return DockerEnvironment(
            info=(
                self._docker_detector.detect()
            ),
            containers=(
                self._container_detector.detect()
            ),
            compose=(
                self._compose_detector.detect(
                    path,
                )
            ),
        )