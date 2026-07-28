from pathlib import Path

from brain.io.readers.docx_reader import DocxReader


def test_docx_reader_reads_docx():

    reader = DocxReader()

    document = reader.read(
        Path("tests/models/sample_files/sample.docx")
    )

    assert document.name == "sample.docx"
    assert document.extension == ".docx"

    assert "Hello Madhav!" in document.content
    assert "first DOCX document" in document.content