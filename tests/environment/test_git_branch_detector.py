from pathlib import Path

from brain.environment.git.git_branch_detector import (
    GitBranchDetector,
)


def test_git_branch_detector():

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

    branch = (
        GitBranchDetector()
        .detect(
            str(
                repository,
            )
        )
    )

    assert (
        branch.name
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

def test_missing_git_branch(
    tmp_path,
):

    branch = (
        GitBranchDetector()
        .detect(
            str(
                tmp_path,
            )
        )
    )

    assert (
        branch.name
        == ""
    )