from pathlib import Path

from brain.workspace.repository_analyzer import (
    RepositoryAnalyzer,
)


def test_repository_analyzer():

    files = [
        Path("pom.xml"),
        Path("README.md"),
        Path("Dockerfile"),
    ]

    analyzer = (
        RepositoryAnalyzer()
    )

    result = analyzer.analyze(
        files,
    )

    assert result == {
        "Maven",
        "Documentation",
        "Docker",
    }