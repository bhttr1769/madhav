from brain.evolution.models.evolution_checkpoint import (
    EvolutionCheckpoint,
)


class EvolutionRollbackManager:
    def __init__(self, git_rollback):
        self._git_rollback = git_rollback

    def can_rollback(
        self,
        checkpoint: EvolutionCheckpoint,
    ) -> bool:
        if not isinstance(
            checkpoint,
            EvolutionCheckpoint,
        ):
            raise TypeError(
                "checkpoint must be an EvolutionCheckpoint"
            )

        if (
            checkpoint.evolution_commit_hash is None
        ):
            return False

        return not (
            checkpoint.has_uncommitted_changes
            or checkpoint.has_untracked_files
        )

    def rollback(
        self,
        checkpoint: EvolutionCheckpoint,
    ) -> str:
        if not isinstance(
            checkpoint,
            EvolutionCheckpoint,
        ):
            raise TypeError(
                "checkpoint must be an EvolutionCheckpoint"
            )

        if not self.can_rollback(checkpoint):
            raise RuntimeError(
                "rollback is unsafe or the evolution "
                "commit is unavailable"
            )

        return self._git_rollback.revert(
            repository_path=checkpoint.repository_path,
            commit_hash=checkpoint.evolution_commit_hash,
        )