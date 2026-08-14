from pathlib import Path

from brain.workspace.repository_fingerprint import (
    RepositoryFingerprint,
)


def test_repository_fingerprint():

    files = [
        Path("src/main.py"),
        Path("src/config.json"),
        Path("docs/README.md"),
    ]

    repository = (
        RepositoryFingerprint()
    ).build(
        files,
    )

    assert (
        repository.files
        == 3
    )

    assert (
        repository.directories
        == 2
    )

    assert (
        len(
            repository.signatures
        )
        > 0
    )