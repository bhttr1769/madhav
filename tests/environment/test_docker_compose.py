from pathlib import Path

from brain.environment.docker.docker_compose_detector import (
    DockerComposeDetector,
)


def test_docker_compose_detector():

    workspace = Path(
        "temp_workspace",
    )

    workspace.mkdir(
        exist_ok=True,
    )

    (
        workspace
        / "docker-compose.yml"
    ).touch()

    compose = (
        DockerComposeDetector()
    ).detect(
        workspace,
    )

    assert (
        compose.exists
        is True
    )

    assert (
        "docker-compose.yml"
        in compose.path
    )