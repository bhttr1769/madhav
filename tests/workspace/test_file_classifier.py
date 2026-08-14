from pathlib import Path

from brain.workspace.file_classifier import (
    FileClassifier,
)


def test_file_classifier():

    classifier = FileClassifier()

    assert (
        classifier.classify(
            Path("main.py")
        )
        == "source"
    )

    assert (
        classifier.classify(
            Path("README.md")
        )
        == "documentation"
    )

    assert (
        classifier.classify(
            Path("config.json")
        )
        == "configuration"
    )

    assert (
        classifier.classify(
            Path("test_app.py")
        )
        == "test"
    )