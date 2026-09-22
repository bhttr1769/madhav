from dataclasses import dataclass


@dataclass(frozen=True)
class EvolutionIntegrationRecovery:
    evolution_id: str
    integration_succeeded: bool
    rollback_required: bool
    reason: str