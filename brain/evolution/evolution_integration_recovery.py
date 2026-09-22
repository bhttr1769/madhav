from brain.evolution.models.evolution_integration_recovery import (
    EvolutionIntegrationRecovery,
)


class EvolutionIntegrationRecoveryManager:
    def recover(
        self,
        evolution_id: str,
        integration_succeeded: bool,
        reason: str,
    ) -> EvolutionIntegrationRecovery:
        if not isinstance(
            evolution_id,
            str,
        ):
            raise TypeError(
                "evolution_id must be a string"
            )

        if not evolution_id.strip():
            raise ValueError(
                "evolution_id must not be empty"
            )

        if not isinstance(
            integration_succeeded,
            bool,
        ):
            raise TypeError(
                "integration_succeeded must be a bool"
            )

        if not isinstance(
            reason,
            str,
        ):
            raise TypeError(
                "reason must be a string"
            )

        if not reason.strip():
            raise ValueError(
                "reason must not be empty"
            )

        return EvolutionIntegrationRecovery(
            evolution_id=evolution_id,
            integration_succeeded=integration_succeeded,
            rollback_required=(
                not integration_succeeded
            ),
            reason=reason,
        )