from dataclasses import dataclass


@dataclass(
    frozen=True,
)
class DockerCompose:
    """
    Represents Docker Compose configuration.
    """

    exists: bool

    path: str