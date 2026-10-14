
from dataclasses import dataclass


@dataclass(frozen=True)
class ReportingRelationship:
    """A direct reporting relationship between two agents."""

    agent_id: str
    manager_agent_id: str

    def __post_init__(self) -> None:
        for field_name in ("agent_id", "manager_agent_id"):
            value = getattr(self, field_name)

            if not isinstance(value, str):
                raise TypeError(f"{field_name} must be a string")

            if not value.strip():
                raise ValueError(f"{field_name} must not be empty")

        if self.agent_id == self.manager_agent_id:
            raise ValueError(
                "an agent cannot report to itself"
            )
