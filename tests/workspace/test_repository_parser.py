from pathlib import Path

from brain.workspace.parsing.repository_parser import (
    RepositoryParser,
)


def create_repository(
    root: Path,
):

    (root / "src").mkdir()

    (root / "tests").mkdir()

    (root / "docs").mkdir()

    (root / "src" / "main.py").write_text(
        "print('hello')",
        encoding="utf-8",
    )

    (root / "tests" / "test_main.py").write_text(
        "def test_main(): pass",
        encoding="utf-8",
    )

    (root / "docs" / "README.md").write_text(
        "# Test",
        encoding="utf-8",
    )

    (root / "requirements.txt").write_text(
        "pytest",
        encoding="utf-8",
    )


def test_repository_parser_discovers_files(
    tmp_path,
):

    create_repository(
        tmp_path,
    )

    repository = (
        RepositoryParser().parse(
            tmp_path,
        )
    )

    names = {
        file.name
        for file in repository.files
    }

    assert "main.py" in names
    assert "test_main.py" in names
    assert "README.md" in names
    assert "requirements.txt" in names


def test_repository_parser_discovers_directories(
    tmp_path,
):

    create_repository(
        tmp_path,
    )

    repository = (
        RepositoryParser().parse(
            tmp_path,
        )
    )

    paths = {
        directory.path
        for directory in repository.directories
    }

    assert str(
        tmp_path / "src"
    ) in paths

    assert str(
        tmp_path / "tests"
    ) in paths


def test_repository_parser_classifies_files(
    tmp_path,
):

    create_repository(
        tmp_path,
    )

    repository = (
        RepositoryParser().parse(
            tmp_path,
        )
    )

    categories = {
        file.name: file.category
        for file in repository.files
    }

    assert (
        categories["main.py"]
        == "source"
    )

    assert (
        categories["test_main.py"]
        == "test"
    )

    assert (
        categories["README.md"]
        == "documentation"
    )

    assert (
        categories["requirements.txt"]
        == "configuration"
    )


def test_repository_parser_preserves_root(
    tmp_path,
):

    create_repository(
        tmp_path,
    )

    repository = (
        RepositoryParser().parse(
            tmp_path,
        )
    )

    assert (
        repository.root
        == str(
            tmp_path.resolve()
        )
    )


def test_repository_parser_preserves_signatures(
    tmp_path,
):

    create_repository(
        tmp_path,
    )

    repository = (
        RepositoryParser().parse(
            tmp_path,
        )
    )

    values = {
        signature.value
        for signature in repository.signatures
    }

    assert "main.py" in values
    assert ".py" in values
    assert "requirements.txt" in values