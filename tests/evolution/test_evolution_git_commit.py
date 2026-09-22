from unittest.mock import patch

import pytest

from brain.evolution.git.evolution_git_commit import (
    EvolutionGitCommit,
)


def test_commit_stages_specific_paths_and_returns_hash():
    committer = EvolutionGitCommit()

    add_result = type(
        "Result",
        (),
        {
            "returncode": 0,
            "stdout": "",
            "stderr": "",
        },
    )()

    commit_result = type(
        "Result",
        (),
        {
            "returncode": 0,
            "stdout": "[main abc123] Evolution",
            "stderr": "",
        },
    )()

    hash_result = type(
        "Result",
        (),
        {
            "returncode": 0,
            "stdout": "abc123\n",
            "stderr": "",
        },
    )()

    with patch(
        "brain.evolution.git.evolution_git_commit.subprocess.run",
        side_effect=[
            add_result,
            commit_result,
            hash_result,
        ],
    ) as mock_run:
        result = committer.commit(
            repository_path="D:\\Madhav",
            message="Evolution evo-001",
            paths=(
                "brain/example.py",
                "tests/test_example.py",
            ),
        )

    assert result == "abc123"

    assert mock_run.call_count == 3

    assert mock_run.call_args_list[0].args[0] == [
        "git",
        "add",
        "--",
        "brain/example.py",
        "tests/test_example.py",
    ]

    assert mock_run.call_args_list[1].args[0] == [
        "git",
        "commit",
        "-m",
        "Evolution evo-001",
    ]

    assert mock_run.call_args_list[2].args[0] == [
        "git",
        "rev-parse",
        "HEAD",
    ]


def test_commit_requires_repository_path():
    committer = EvolutionGitCommit()

    with pytest.raises(TypeError):
        committer.commit(
            repository_path=123,
            message="Evolution",
            paths=("brain/example.py",),
        )


def test_commit_rejects_empty_repository_path():
    committer = EvolutionGitCommit()

    with pytest.raises(ValueError):
        committer.commit(
            repository_path="",
            message="Evolution",
            paths=("brain/example.py",),
        )


def test_commit_requires_message():
    committer = EvolutionGitCommit()

    with pytest.raises(ValueError):
        committer.commit(
            repository_path="D:\\Madhav",
            message="",
            paths=("brain/example.py",),
        )


def test_commit_requires_paths_tuple():
    committer = EvolutionGitCommit()

    with pytest.raises(TypeError):
        committer.commit(
            repository_path="D:\\Madhav",
            message="Evolution",
            paths=["brain/example.py"],
        )


def test_commit_rejects_empty_paths():
    committer = EvolutionGitCommit()

    with pytest.raises(ValueError):
        committer.commit(
            repository_path="D:\\Madhav",
            message="Evolution",
            paths=(),
        )


def test_commit_rejects_empty_path_value():
    committer = EvolutionGitCommit()

    with pytest.raises(ValueError):
        committer.commit(
            repository_path="D:\\Madhav",
            message="Evolution",
            paths=("",),
        )


def test_commit_raises_when_git_add_fails():
    committer = EvolutionGitCommit()

    failed_result = type(
        "Result",
        (),
        {
            "returncode": 1,
            "stdout": "",
            "stderr": "add failed",
        },
    )()

    with patch(
        "brain.evolution.git.evolution_git_commit.subprocess.run",
        return_value=failed_result,
    ):
        with pytest.raises(RuntimeError):
            committer.commit(
                repository_path="D:\\Madhav",
                message="Evolution",
                paths=("brain/example.py",),
            )


def test_commit_raises_when_git_commit_fails():
    committer = EvolutionGitCommit()

    add_result = type(
        "Result",
        (),
        {
            "returncode": 0,
            "stdout": "",
            "stderr": "",
        },
    )()

    failed_commit = type(
        "Result",
        (),
        {
            "returncode": 1,
            "stdout": "",
            "stderr": "commit failed",
        },
    )()

    with patch(
        "brain.evolution.git.evolution_git_commit.subprocess.run",
        side_effect=[
            add_result,
            failed_commit,
        ],
    ):
        with pytest.raises(RuntimeError):
            committer.commit(
                repository_path="D:\\Madhav",
                message="Evolution",
                paths=("brain/example.py",),
            )


def test_commit_raises_when_hash_lookup_fails():
    committer = EvolutionGitCommit()

    success_result = type(
        "Result",
        (),
        {
            "returncode": 0,
            "stdout": "",
            "stderr": "",
        },
    )()

    failed_hash = type(
        "Result",
        (),
        {
            "returncode": 1,
            "stdout": "",
            "stderr": "hash lookup failed",
        },
    )()

    with patch(
        "brain.evolution.git.evolution_git_commit.subprocess.run",
        side_effect=[
            success_result,
            success_result,
            failed_hash,
        ],
    ):
        with pytest.raises(RuntimeError):
            committer.commit(
                repository_path="D:\\Madhav",
                message="Evolution",
                paths=("brain/example.py",),
            )