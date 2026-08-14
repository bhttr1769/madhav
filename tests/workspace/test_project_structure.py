from pathlib import Path

from brain.workspace.project_structure import (
    ProjectStructure,
)


def test_project_structure():

    files = [
        Path("src/main.py"),
        Path("src/config.json"),
        Path("tests/test_app.py"),
        Path("docs/README.md"),
    ]

    structure = ProjectStructure()

    directories = structure.directories(
        files,
    )

    assert directories == {
        Path("src"),
        Path("tests"),
        Path("docs"),
    }