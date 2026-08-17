from dataclasses import dataclass


@dataclass(
    frozen=True,
)
class DockerContainer:
    """
    Represents a Docker container.
    """

    container_id: str

    image: str

    name: str

    status: str