
from dataclasses import dataclass


@dataclass(frozen=True)
class Organization:
    """Immutable identity and name of an AI organization."""

    id: str
    name: str

    def __post_init__(self) -> None:
        if not isinstance(self.id, str):
            raise TypeError("id must be a string")

        if not self.id.strip():
            raise ValueError("id must not be empty")

        if not isinstance(self.name, str):
            raise TypeError("name must be a string")

        if not self.name.strip():
            raise ValueError("name must not be empty")
