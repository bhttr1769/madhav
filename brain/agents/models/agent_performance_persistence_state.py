from dataclasses import dataclass

from brain.agents.models.agent_performance_record import (
    AgentPerformanceRecord,
)


@dataclass(frozen=True)
class AgentPerformancePersistenceState:
    agent_id: str
    record: AgentPerformanceRecord

    def __post_init__(self) -> None:
        if not isinstance(self.agent_id, str):
            raise TypeError("agent_id must be a string")

        if not self.agent_id.strip():
            raise ValueError("agent_id must not be empty")

        if not isinstance(
            self.record,
            AgentPerformanceRecord,
        ):
            raise TypeError(
                "record must be an AgentPerformanceRecord"
            )

        if self.record.agent_id != self.agent_id:
            raise ValueError(
                "record agent_id must match persistence agent_id"
            )