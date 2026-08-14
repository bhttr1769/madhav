from brain.workspace.discovery.workspace_scanner import (
    WorkspaceScanner,
)


def test_workspace_scanner(
    tmp_path,
):

    project = tmp_path / "project"

    project.mkdir()

    (project / "main.py").write_text(
        "print('hello')"
    )

    (project / "pom.xml").write_text(
        "<project></project>"
    )

    docs = project / "docs"

    docs.mkdir()

    (docs / "README.md").write_text(
        "documentation"
    )

    files = WorkspaceScanner().scan(
        project,
    )

    assert len(files) == 3