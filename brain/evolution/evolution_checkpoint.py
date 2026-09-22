from brain.evolution.models.evolution_checkpoint import EvolutionCheckpoint


class EvolutionCheckpointManager:
    ACTIVE = "active"
    COMPLETED = "completed"
    FAILED = "failed"

    def __init__(self, git_service):
        self._git_service = git_service
        self._checkpoints: dict[str, EvolutionCheckpoint] = {}

    def create(
        self,
        evolution_id: str,
        repository_path: str,
    ) -> EvolutionCheckpoint:
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
            repository_path,
            str,
        ):
            raise TypeError(
                "repository_path must be a string"
            )

        if not repository_path.strip():
            raise ValueError(
                "repository_path must not be empty"
            )

        if evolution_id in self._checkpoints:
            raise ValueError(
                "checkpoint already exists for evolution_id: "
                f"{evolution_id}"
            )

        repository = self._git_service.repository(
            repository_path,
        )

        if not repository.is_repository:
            raise ValueError(
                "repository_path must point to "
                "a Git repository"
            )

        branch = self._git_service.branch(
            repository_path,
        )

        status = self._git_service.status(
            repository_path,
        )

        commit = self._git_service.commit(
            repository_path,
        )

        checkpoint = EvolutionCheckpoint(
            evolution_id=evolution_id,
            repository_path=repository_path,
            branch=branch.name,
            commit_hash=commit.hash,
            has_uncommitted_changes=(
                status.has_uncommitted_changes
            ),
            has_untracked_files=(
                status.has_untracked_files
            ),
            status=self.ACTIVE,
        )

        self._checkpoints[evolution_id] = checkpoint

        return checkpoint

    def get(
        self,
        evolution_id: str,
    ) -> EvolutionCheckpoint:
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

        try:
            return self._checkpoints[evolution_id]
        except KeyError:
            raise KeyError(
                "checkpoint not found for evolution_id: "
                f"{evolution_id}"
            )

    def complete(
        self,
        evolution_id: str,
    ) -> EvolutionCheckpoint:
        checkpoint = self.get(evolution_id)

        if checkpoint.status != self.ACTIVE:
            raise ValueError(
                "only active checkpoints can be completed"
            )

        completed = EvolutionCheckpoint(
            evolution_id=checkpoint.evolution_id,
            repository_path=checkpoint.repository_path,
            branch=checkpoint.branch,
            commit_hash=checkpoint.commit_hash,
            has_uncommitted_changes=(
                checkpoint.has_uncommitted_changes
            ),
            has_untracked_files=(
                checkpoint.has_untracked_files
            ),
            status=self.COMPLETED,
        )

        self._checkpoints[evolution_id] = completed

        return completed

    def fail(
        self,
        evolution_id: str,
    ) -> EvolutionCheckpoint:
        checkpoint = self.get(evolution_id)

        if checkpoint.status != self.ACTIVE:
            raise ValueError(
                "only active checkpoints can be failed"
            )

        failed = EvolutionCheckpoint(
            evolution_id=checkpoint.evolution_id,
            repository_path=checkpoint.repository_path,
            branch=checkpoint.branch,
            commit_hash=checkpoint.commit_hash,
            has_uncommitted_changes=(
                checkpoint.has_uncommitted_changes
            ),
            has_untracked_files=(
                checkpoint.has_untracked_files
            ),
            status=self.FAILED,
        )

        self._checkpoints[evolution_id] = failed

        return failed