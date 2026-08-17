from brain.environment.git.git_status import (
    GitStatus,
)


def test_git_status():

    status = GitStatus(
        branch="main",
        has_uncommitted_changes=False,
        has_untracked_files=False,
    )

    assert (
        status.branch
        == "main"
    )

    assert (
        status.has_uncommitted_changes
        is False
    )

    assert (
        status.has_untracked_files
        is False
    )