from pathlib import Path

from brain.workspace.project_summary import (
    ProjectSummary,
)


def test_project_summary():

    files = [
        Path("src/main.py"),
        Path("src/config.json"),
        Path("docs/README.md"),
        Path("pom.xml"),
    ]

    summary = (
        ProjectSummary()
    ).build(files)

    assert (
        summary["file_count"]
        == 4
    )

    assert (
        summary["technologies"]
        == {
            "Python",
            "JSON",
            "Markdown",
        }
    )

    assert (
        summary["directories"]
        == {
            Path("."),
            Path("src"),
            Path("docs"),
        }
    )
    
    assert (
        summary["repository"]
        == {
            "Documentation",
            "Maven",
        }
    )