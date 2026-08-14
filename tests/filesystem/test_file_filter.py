from pathlib import Path

from brain.filesystem.file_filter import (
    FileFilter,
)


def test_filter_by_extension():

    files = [
        Path("notes.txt"),
        Path("book.pdf"),
        Path("resume.docx"),
        Path("guide.pdf"),
    ]

    filter_service = FileFilter()

    pdfs = filter_service.by_extension(
        files,
        ".pdf",
    )

    assert len(pdfs) == 2

    assert Path("book.pdf") in pdfs

    assert Path("guide.pdf") in pdfs