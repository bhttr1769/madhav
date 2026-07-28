from pathlib import Path

from brain.factory.document_factory import DocumentFactory


def test_document_factory_creates_document():

    document = DocumentFactory.create(
        Path("tests/models/sample.txt"),
        "Hello Madhav!"
    )

    assert document.name == "sample.txt"
    assert document.extension == ".txt"
    assert document.content == "Hello Madhav!"
    assert document.size > 0