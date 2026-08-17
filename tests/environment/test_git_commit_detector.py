from pathlib import Path

from brain.environment.git.git_commit_detector import (
    GitCommitDetector,
)


def test_git_commit_detector():

    repository = Path(
        "temp_repository",
    )

    (
        repository
        / ".git"
    ).mkdir(
        parents=True,
        exist_ok=True,
    )

    (
        repository
        / ".git"
        / "HEAD"
    ).write_text(
        "abc123",
    )

    commit = (
        GitCommitDetector()
        .detect(
            str(
                repository,
            )
        )
    )

    assert (
        commit.hash
        == "abc123"
    )

    (
        repository
        / ".git"
        / "HEAD"
    ).unlink()

    (
        repository
        / ".git"
    ).rmdir()

    repository.rmdir()