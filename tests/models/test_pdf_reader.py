from pathlib import Path

from brain.io.readers.pdf_reader import PDFReader


def test_pdf_reader_reads_pdf():

    reader = PDFReader()

    document = reader.read(
        Path("tests/models/sample_files/sample.pdf")
    )

    assert document.name == "sample.pdf"
    assert document.extension == ".pdf"

    assert "Hello Madhav!" in document.content
    assert "first PDF document" in document.content