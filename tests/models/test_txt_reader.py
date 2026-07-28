from pathlib import Path

from brain.io.readers.txt_reader import TXTReader


def test_txt_reader():

    reader = TXTReader()

    doc = reader.read(Path("tests/models/sample.txt"))

    assert doc.name == "sample.txt"
    assert doc.extension == ".txt"
    assert "Hello Madhav!" in doc.content