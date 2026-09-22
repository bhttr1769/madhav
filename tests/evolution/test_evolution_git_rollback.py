from unittest.mock import patch

import pytest

from brain.evolution.git.evolution_git_rollback import (
    EvolutionGitRollback,
)


def test_revert_executes_git_revert():
    rollback = EvolutionGitRollback()

    mock_result = type(
        "Result",
        (),
        {
            "returncode": 0,
            "stdout": "Reverted evolution commit",
            "stderr": "",
        },
    )()

    with patch(
        "brain.evolution.git.evolution_git_rollback.subprocess.run",
        return_value=mock_result,
    ) as mock_run:
        result = rollback.revert(
            repository_path="D:\\Madhav",
            commit_hash="def456",
        )

    assert result == "Reverted evolution commit"

    mock_run.assert_called_once_with(
        [
            "git",
            "revert",
            "--no-edit",
            "def456",
        ],
        cwd="D:\\Madhav",
        capture_output=True,
        text=True,
    )


def test_revert_rejects_non_string_repository_path():
    rollback = EvolutionGitRollback()

    with pytest.raises(TypeError):
        rollback.revert(
            repository_path=123,
            commit_hash="def456",
        )


def test_revert_rejects_empty_repository_path():
    rollback = EvolutionGitRollback()

    with pytest.raises(ValueError):
        rollback.revert(
            repository_path="",
            commit_hash="def456",
        )


def test_revert_rejects_non_string_commit_hash():
    rollback = EvolutionGitRollback()

    with pytest.raises(TypeError):
        rollback.revert(
            repository_path="D:\\Madhav",
            commit_hash=123,
        )


def test_revert_rejects_empty_commit_hash():
    rollback = EvolutionGitRollback()

    with pytest.raises(ValueError):
        rollback.revert(
            repository_path="D:\\Madhav",
            commit_hash="",
        )


def test_revert_raises_when_git_fails():
    rollback = EvolutionGitRollback()

    mock_result = type(
        "Result",
        (),
        {
            "returncode": 1,
            "stdout": "",
            "stderr": "revert failed",
        },
    )()

    with patch(
        "brain.evolution.git.evolution_git_rollback.subprocess.run",
        return_value=mock_result,
    ):
        with pytest.raises(RuntimeError):
            rollback.revert(
                repository_path="D:\\Madhav",
                commit_hash="def456",
            )