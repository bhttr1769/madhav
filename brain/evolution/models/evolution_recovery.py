from dataclasses import dataclass


@dataclass(frozen=True)
class EvolutionRecovery:
    evolution_id: str
    recovered: bool
    recovery_reason: str