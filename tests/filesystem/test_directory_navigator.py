from brain.filesystem.directory_navigator import (
    DirectoryNavigator,
)


def test_directory_navigator(
    tmp_path,
):

    documents = tmp_path / "documents"

    notes = tmp_path / "notes"

    file = tmp_path / "file.txt"

    documents.mkdir()

    notes.mkdir()

    file.write_text(
        "hello"
    )

    navigator = DirectoryNavigator()

    directories = navigator.directories(
        tmp_path
    )

    assert len(directories) == 2

    assert documents in directories

    assert notes in directories