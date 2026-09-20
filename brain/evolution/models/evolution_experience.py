from dataclasses import dataclass


@dataclass(frozen=True)
class EvolutionExperience:
    evolution_id: str
    requested_capability: str
    task_id: str
    task_description: str
    outcome: str
    lesson: str
    reusable: bool