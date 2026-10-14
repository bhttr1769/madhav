
from dataclasses import dataclass


@dataclass(frozen=True)
class OrganizationalUnit:
    """An organizational unit within an organization."""

    id: str
    organization_id: str
    name: str
    parent_unit_id: str | None = None

    def __post_init__(self) -> None:
        for field_name in ("id", "organization_id", "name"):
            value = getattr(self, field_name)

            if not isinstance(value, str):
                raise TypeError(f"{field_name} must be a string")

            if not value.strip():
                raise ValueError(f"{field_name} must not be empty")

        if self.parent_unit_id is not None:
            if not isinstance(self.parent_unit_id, str):
                raise TypeError(
                    "parent_unit_id must be a string or None"
                )

            if not self.parent_unit_id.strip():
                raise ValueError(
                    "parent_unit_id must not be empty when provided"
                )

            if self.parent_unit_id == self.id:
                raise ValueError(
                    "an organizational unit cannot be its own parent"
                )
