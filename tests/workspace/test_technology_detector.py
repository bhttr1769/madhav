from pathlib import Path

from brain.workspace.technology_detector import (
    TechnologyDetector,
)


def test_technology_detector():

    files = [
        Path("main.py"),
        Path("app.java"),
        Path("config.json"),
        Path("README.md"),
        Path("script.js"),
    ]

    detector = TechnologyDetector()

    technologies = detector.detect(
        files,
    )

    assert technologies == {
        "Python",
        "Java",
        "JavaScript",
        "JSON",
        "Markdown",
    }