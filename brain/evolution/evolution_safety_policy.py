from brain.evolution.evolution_checkpoint import (
    EvolutionCheckpointManager,
)
from brain.evolution.models.evolution_checkpoint import (
    EvolutionCheckpoint,
)


class EvolutionSafetyPolicy:
    def validate_autonomous_execution(
        self,
        checkpoint: EvolutionCheckpoint,
    ) -> None:
        if not isinstance(
            checkpoint,
            EvolutionCheckpoint,
        ):
            raise TypeError(
                "checkpoint must be an EvolutionCheckpoint"
            )

        if checkpoint.status != EvolutionCheckpointManager.ACTIVE:
            raise ValueError(
                "autonomous evolution requires an active checkpoint"
            )

        if checkpoint.has_uncommitted_changes:
            raise RuntimeError(
                "autonomous evolution is unsafe because "
                "the repository has uncommitted changes"
            )

        if checkpoint.has_untracked_files:
            raise RuntimeError(
                "autonomous evolution is unsafe because "
                "the repository has untracked files"
            )