from pathlib import Path

from brain.filesystem.directory_scanner import (
    DirectoryScanner,
)


def test_directory_scanner(
    tmp_path,
):

    file1 = tmp_path / "file1.txt"
    file2 = tmp_path / "file2.pdf"

    file1.write_text("Hello")

    file2.write_text("World")

    scanner = DirectoryScanner()

    files = scanner.scan(
        tmp_path,
    )

    assert len(files) == 2

    assert file1 in files

    assert file2 in files