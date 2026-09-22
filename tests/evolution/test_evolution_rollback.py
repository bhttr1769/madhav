import pytest

from brain.evolution.evolution_rollback import (
    EvolutionRollbackManager,
)
from brain.evolution.models.evolution_checkpoint import (
    EvolutionCheckpoint,
)


class FakeGitRollback:
    def __init__(self, result="rollback complete"):
        self.result = result
        self.calls = []

    def revert(
        self,
        repository_path,
        commit_hash,
    ):
        self.calls.append(
            (
                repository_path,
                commit_hash,
            )
        )
        return self.result


def clean_checkpoint():
    return EvolutionCheckpoint(
        evolution_id="evo-001",
        repository_path="D:\\Madhav",
        branch="main",
        commit_hash="abc123",
        has_uncommitted_changes=False,
        has_untracked_files=False,
        status="active",
        evolution_commit_hash="def456",
    )


def checkpoint_without_evolution_commit():
    return EvolutionCheckpoint(
        evolution_id="evo-002",
        repository_path="D:\\Madhav",
        branch="main",
        commit_hash="abc123",
        has_uncommitted_changes=False,
        has_untracked_files=False,
        status="active",
        evolution_commit_hash=None,
    )


def dirty_checkpoint():
    return EvolutionCheckpoint(
        evolution_id="evo-003",
        repository_path="D:\\Madhav",
        branch="main",
        commit_hash="abc123",
        has_uncommitted_changes=True,
        has_untracked_files=False,
        status="active",
        evolution_commit_hash="def456",
    )


def untracked_checkpoint():
    return EvolutionCheckpoint(
        evolution_id="evo-004",
        repository_path="D:\\Madhav",
        branch="main",
        commit_hash="abc123",
        has_uncommitted_changes=False,
        has_untracked_files=True,
        status="active",
        evolution_commit_hash="def456",
    )


def test_clean_checkpoint_with_evolution_commit_allows_rollback():
    manager = EvolutionRollbackManager(
        FakeGitRollback()
    )

    assert manager.can_rollback(
        clean_checkpoint()
    ) is True


def test_checkpoint_without_evolution_commit_blocks_rollback():
    manager = EvolutionRollbackManager(
        FakeGitRollback()
    )

    assert manager.can_rollback(
        checkpoint_without_evolution_commit()
    ) is False


def test_preexisting_uncommitted_changes_block_rollback():
    manager = EvolutionRollbackManager(
        FakeGitRollback()
    )

    assert manager.can_rollback(
        dirty_checkpoint()
    ) is False


def test_preexisting_untracked_files_block_rollback():
    manager = EvolutionRollbackManager(
        FakeGitRollback()
    )

    assert manager.can_rollback(
        untracked_checkpoint()
    ) is False


def test_rollback_uses_evolution_commit_not_baseline_commit():
    git_rollback = FakeGitRollback()

    manager = EvolutionRollbackManager(
        git_rollback
    )

    checkpoint = clean_checkpoint()

    result = manager.rollback(checkpoint)

    assert result == "rollback complete"
    assert git_rollback.calls == [
        (
            "D:\\Madhav",
            "def456",
        )
    ]


def test_rollback_never_uses_baseline_commit():
    git_rollback = FakeGitRollback()

    manager = EvolutionRollbackManager(
        git_rollback
    )

    checkpoint = clean_checkpoint()

    manager.rollback(checkpoint)

    assert git_rollback.calls[0][1] != (
        checkpoint.commit_hash
    )


def test_rollback_rejects_unsafe_checkpoint():
    manager = EvolutionRollbackManager(
        FakeGitRollback()
    )

    with pytest.raises(RuntimeError):
        manager.rollback(
            dirty_checkpoint()
        )


def test_rollback_rejects_checkpoint_without_evolution_commit():
    manager = EvolutionRollbackManager(
        FakeGitRollback()
    )

    with pytest.raises(RuntimeError):
        manager.rollback(
            checkpoint_without_evolution_commit()
        )


def test_rollback_requires_checkpoint():
    manager = EvolutionRollbackManager(
        FakeGitRollback()
    )

    with pytest.raises(TypeError):
        manager.rollback(None)