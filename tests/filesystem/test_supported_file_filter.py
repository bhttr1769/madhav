from pathlib import Path

from brain.filesystem.supported_file_filter import (
    SupportedFileFilter,
)


def test_supported_file_filter():

    files = [
        Path("notes.pdf"),
        Path("report.docx"),
        Path("text.txt"),
        Path("image.png"),
        Path("video.mp4"),
        Path("archive.zip"),
    ]

    filter_service = (
        SupportedFileFilter()
    )

    supported = (
        filter_service.filter(
            files,
        )
    )

    assert len(supported) == 3

    assert Path(
        "notes.pdf"
    ) in supported

    assert Path(
        "report.docx"
    ) in supported

    assert Path(
        "text.txt"
    ) in supported