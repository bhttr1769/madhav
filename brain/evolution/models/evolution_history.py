from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class EvolutionHistory:
    evolution_id: str
    requested_capability: str
    objective: str
    mode: str
    status: str
    started_at: datetime
    completed_at: datetime | None
    task_count: int
    completed_task_count: int
    passed: bool
    termination_reason: str