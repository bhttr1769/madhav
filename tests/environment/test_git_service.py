from pathlib import Path

from brain.environment.git.git_service import (
    GitService,
)


def test_git_service():

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
        "ref: refs/heads/main",
    )

    service = (
        GitService()
    )

    assert (
        service.repository(
            str(repository),
        ).is_repository
    )

    assert (
        service.branch(
            str(repository),
        ).name
        == "main"
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