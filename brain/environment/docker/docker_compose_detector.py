from pathlib import Path

from brain.environment.docker.docker_compose import (
    DockerCompose,
)


class DockerComposeDetector:

    def detect(
        self,
        path=".",
    ) -> DockerCompose:

        workspace = Path(
            path,
        )

        compose_files = [
            "docker-compose.yml",
            "docker-compose.yaml",
            "compose.yml",
            "compose.yaml",
        ]

        for filename in compose_files:

            compose_path = (
                workspace
                / filename
            )

            if compose_path.exists():

                return DockerCompose(
                    exists=True,
                    path=str(
                        compose_path,
                    ),
                )

        return DockerCompose(
            exists=False,
            path="",
        )