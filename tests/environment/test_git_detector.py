from pathlib import Path

from brain.environment.git.git_detector import (
    GitDetector,
)


def test_git_detector():

    repository = (
        GitDetector()
    ).detect(
        ".",
    )

    assert (
        isinstance(
            repository.path,
            str,
        )
    )

    assert (
        isinstance(
            repository.is_repository,
            bool,
        )
    )


def test_detect_current_repository():

    repository = (
        GitDetector()
    ).detect(
        str(
            Path.cwd(),
        )
    )

    assert (
        repository.is_repository
    )