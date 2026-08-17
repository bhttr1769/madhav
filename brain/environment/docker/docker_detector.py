import shutil

from brain.environment.docker.docker_info import (
    DockerInfo,
)


class DockerDetector:

    def detect(
        self,
    ) -> DockerInfo:

        return DockerInfo(
            installed=(
                shutil.which(
                    "docker",
                )
                is not None
            ),
        )