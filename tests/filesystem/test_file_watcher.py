from brain.filesystem.file_watcher import (
    FileWatcher,
)


def test_file_watcher(
    tmp_path,
):

    file = tmp_path / "notes.txt"

    file.write_text(
        "hello"
    )

    watcher = FileWatcher()

    modified = watcher.modified_at(
        file,
    )

    assert modified is not None