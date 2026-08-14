from pathlib import Path

from brain.workspace.project_analyzer import (
    ProjectAnalyzer,
)


def test_project_file_count():

    files = [
        Path("main.py"),
        Path("config.json"),
        Path("README.md"),
    ]

    analyzer = ProjectAnalyzer()

    assert analyzer.file_count(
        files,
    ) == 3