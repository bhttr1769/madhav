from dataclasses import dataclass


@dataclass(
    frozen=True,
)
class DockerInfo:

    installed: bool