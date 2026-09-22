from brain.evolution.models.evolution_recovery import EvolutionRecovery


class EvolutionRecoveryManager:
    def recover(
        self,
        evolution_id: str,
        reason: str,
    ) -> EvolutionRecovery:
        if not isinstance(evolution_id, str):
            raise TypeError("evolution_id must be a string")

        if not evolution_id.strip():
            raise ValueError("evolution_id must not be empty")

        if not isinstance(reason, str):
            raise TypeError("reason must be a string")

        if not reason.strip():
            raise ValueError("reason must not be empty")

        return EvolutionRecovery(
            evolution_id=evolution_id,
            recovered=False,
            recovery_reason=reason,
        )