import pytest

from brain.evolution.evolution_integration_recovery import (
    EvolutionIntegrationRecoveryManager,
)
from brain.evolution.evolution_integration_recovery_coordinator import (
    EvolutionIntegrationRecoveryCoordinator,
)
from brain.evolution.evolution_rollback import (
    EvolutionRollbackManager,
)
from brain.evolution.models.evolution_checkpoint import (
    EvolutionCheckpoint,
)


class FakeGitRollback:
    def __init__(self):
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

        return "rollback complete"


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


def dirty_checkpoint():
    return EvolutionCheckpoint(
        evolution_id="evo-002",
        repository_path="D:\\Madhav",
        branch="main",
        commit_hash="abc123",
        has_uncommitted_changes=True,
        has_untracked_files=False,
        status="active",
        evolution_commit_hash="def456",
    )


def build_coordinator(git_rollback):
    recovery_manager = (
        EvolutionIntegrationRecoveryManager()
    )

    rollback_manager = EvolutionRollbackManager(
        git_rollback
    )

    return EvolutionIntegrationRecoveryCoordinator(
        recovery_manager=recovery_manager,
        rollback_manager=rollback_manager,
    )


def test_failed_integration_triggers_rollback():
    git_rollback = FakeGitRollback()

    coordinator = build_coordinator(
        git_rollback
    )

    recovery = coordinator.recover(
        checkpoint=clean_checkpoint(),
        reason="capability integration failed",
    )

    assert recovery.integration_succeeded is False
    assert recovery.rollback_required is True

    assert git_rollback.calls == [
        (
            "D:\\Madhav",
            "def456",
        )
    ]


def test_failed_integration_with_unsafe_checkpoint_is_rejected():
    git_rollback = FakeGitRollback()

    coordinator = build_coordinator(
        git_rollback
    )

    with pytest.raises(RuntimeError):
        coordinator.recover(
            checkpoint=dirty_checkpoint(),
            reason="capability integration failed",
        )

    assert git_rollback.calls == []


def test_rollback_uses_evolution_commit():
    git_rollback = FakeGitRollback()

    coordinator = build_coordinator(
        git_rollback
    )

    checkpoint = clean_checkpoint()

    coordinator.recover(
        checkpoint=checkpoint,
        reason="integration failed",
    )

    assert git_rollback.calls[0][1] == (
        checkpoint.evolution_commit_hash
    )

    assert git_rollback.calls[0][1] != (
        checkpoint.commit_hash
    )


def test_requires_checkpoint():
    git_rollback = FakeGitRollback()

    coordinator = build_coordinator(
        git_rollback
    )

    with pytest.raises(TypeError):
        coordinator.recover(
            checkpoint=None,
            reason="integration failed",
        )