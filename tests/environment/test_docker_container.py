from brain.environment.docker.docker_container import (
    DockerContainer,
)


def test_docker_container():

    container = DockerContainer(
        container_id="123",
        image="postgres:16",
        name="postgres",
        status="running",
    )

    assert (
        container.container_id
        == "123"
    )

    assert (
        container.image
        == "postgres:16"
    )

    assert (
        container.name
        == "postgres"
    )

    assert (
        container.status
        == "running"
    )