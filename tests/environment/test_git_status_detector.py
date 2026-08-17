from pathlib import Path

from brain.environment.git.git_status_detector import (
    GitStatusDetector,
)


def test_git_status_detector():

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

    status = (
        GitStatusDetector()
        .detect(
            str(
                repository,
            )
        )
    )

    assert (
        status.is_clean
        is True
    )

    (
        repository
        / ".git"
    ).rmdir()

    repository.rmdir()