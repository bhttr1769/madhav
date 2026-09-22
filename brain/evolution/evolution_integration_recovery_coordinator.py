from brain.evolution.models.evolution_checkpoint import (
    EvolutionCheckpoint,
)
from brain.evolution.evolution_integration_recovery import (
    EvolutionIntegrationRecoveryManager,
)
from brain.evolution.evolution_rollback import (
    EvolutionRollbackManager,
)


class EvolutionIntegrationRecoveryCoordinator:
    def __init__(
        self,
        recovery_manager: EvolutionIntegrationRecoveryManager,
        rollback_manager: EvolutionRollbackManager,
    ):
        self._recovery_manager = recovery_manager
        self._rollback_manager = rollback_manager

    def recover(
        self,
        checkpoint: EvolutionCheckpoint,
        reason: str,
    ):
        if not isinstance(
            checkpoint,
            EvolutionCheckpoint,
        ):
            raise TypeError(
                "checkpoint must be an EvolutionCheckpoint"
            )

        recovery = self._recovery_manager.recover(
            evolution_id=checkpoint.evolution_id,
            integration_succeeded=False,
            reason=reason,
        )

        if not recovery.rollback_required:
            return recovery

        if not self._rollback_manager.can_rollback(
            checkpoint
        ):
            raise RuntimeError(
                "integration failed but rollback "
                "is unsafe"
            )

        self._rollback_manager.rollback(
            checkpoint
        )

        return recovery