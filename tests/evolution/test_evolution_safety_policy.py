import pytest

from brain.evolution.evolution_checkpoint import (
    EvolutionCheckpointManager,
)
from brain.evolution.evolution_safety_policy import (
    EvolutionSafetyPolicy,
)
from brain.evolution.models.evolution_checkpoint import (
    EvolutionCheckpoint,
)


def checkpoint(
    *,
    has_uncommitted_changes=False,
    has_untracked_files=False,
    status=EvolutionCheckpointManager.ACTIVE,
):
    return EvolutionCheckpoint(
        evolution_id="evo-test-001",
        repository_path="D:/Madhav",
        branch="main",
        commit_hash="abc123",
        has_uncommitted_changes=has_uncommitted_changes,
        has_untracked_files=has_untracked_files,
        status=status,
        evolution_commit_hash=None,
    )


def test_clean_repository_is_allowed():
    policy = EvolutionSafetyPolicy()

    policy.validate_autonomous_execution(
        checkpoint()
    )


def test_uncommitted_changes_are_rejected():
    policy = EvolutionSafetyPolicy()

    with pytest.raises(
        RuntimeError,
        match="uncommitted changes",
    ):
        policy.validate_autonomous_execution(
            checkpoint(
                has_uncommitted_changes=True,
            )
        )


def test_untracked_files_are_rejected():
    policy = EvolutionSafetyPolicy()

    with pytest.raises(
        RuntimeError,
        match="untracked files",
    ):
        policy.validate_autonomous_execution(
            checkpoint(
                has_untracked_files=True,
            )
        )


def test_non_active_checkpoint_is_rejected():
    policy = EvolutionSafetyPolicy()

    with pytest.raises(
        ValueError,
        match="active checkpoint",
    ):
        policy.validate_autonomous_execution(
            checkpoint(
                status=EvolutionCheckpointManager.COMPLETED,
            )
        )


def test_invalid_checkpoint_is_rejected():
    policy = EvolutionSafetyPolicy()

    with pytest.raises(
        TypeError,
        match="EvolutionCheckpoint",
    ):
        policy.validate_autonomous_execution(
            object()
        )