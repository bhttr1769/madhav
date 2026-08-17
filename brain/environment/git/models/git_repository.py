from dataclasses import dataclass


@dataclass(
    frozen=True,
)
class GitRepository:

    path: str

    is_repository: bool