
from dataclasses import dataclass


@dataclass(frozen=True)
class OrganizationalRole:
    """A named role within an organization, without permission semantics."""

    id: str
    organization_id: str
    name: str

    def __post_init__(self) -> None:
        for field_name in ("id", "organization_id", "name"):
            value = getattr(self, field_name)

            if not isinstance(value, str):
                raise TypeError(f"{field_name} must be a string")

            if not value.strip():
                raise ValueError(f"{field_name} must not be empty")
