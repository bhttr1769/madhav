from pathlib import Path

from brain.filesystem.file_search import (
    FileSearch,
)


def test_search_files_by_name():

    files = [
        Path("java_notes.pdf"),
        Path("spring_boot.docx"),
        Path("python_guide.txt"),
        Path("advanced_java.pdf"),
    ]

    search = FileSearch()

    results = search.by_name(
        files,
        "java",
    )

    assert len(results) == 2

    assert Path(
        "java_notes.pdf"
    ) in results

    assert Path(
        "advanced_java.pdf"
    ) in results