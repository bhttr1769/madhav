from pathlib import Path

from brain.workspace.workspace_learner import (
    WorkspaceLearner,
)


class FakeBrain:

    def __init__(self):

        self.learned = []

    def learn(
        self,
        file,
    ):

        self.learned.append(
            file
        )


def test_workspace_learner(
    tmp_path,
):

    project = tmp_path / "project"

    project.mkdir()

    (project / "main.py").write_text(
        "print('hello')"
    )

    (project / "README.md").write_text(
        "docs"
    )

    learner = WorkspaceLearner(
        FakeBrain(),
    )

    summary = learner.learn(
        project,
    )

    assert (
        summary["file_count"]
        == 2
    )