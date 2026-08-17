from brain.environment.docker.docker_container import (
    DockerContainer,
)

from brain.environment.models.command import (
    Command,
)


class DockerContainerDetector:

    def __init__(
        self,
        terminal,
    ):

        self._terminal = terminal

    def detect(
        self,
    ) -> list[DockerContainer]:

        result = (
            self._terminal.execute(
                Command(
                    (
                        "docker ps "
                        "--format "
                        '"{{.ID}}|{{.Image}}|'
                        '{{.Names}}|{{.Status}}"'
                    ),
                ),
            )
        )

        if result.return_code != 0:

            return []

        containers = []

        for line in (
            result.stdout
            .splitlines()
        ):

            parts = (
                line.split(
                    "|",
                )
            )

            if len(parts) != 4:

                continue

            containers.append(
                DockerContainer(
                    container_id=parts[0],
                    image=parts[1],
                    name=parts[2],
                    status=parts[3],
                )
            )

        return containers