from pathlib import Path

from brain.workspace.workspace_learner import (
    WorkspaceLearner,
)

from brain.workspace.workspace_summary_builder import (
    WorkspaceSummaryBuilder,
)

from brain.workspace.models.workspace import (
    Workspace,
)


class WorkspaceManager:

    def __init__(
        self,
        learner: WorkspaceLearner,
    ):

        self._learner = learner

        self._summary_builder = (
            WorkspaceSummaryBuilder()
        )

    def learn(
        self,
        workspace: str | Path,
    ) -> Workspace:

        return (
            self._learner.learn(
                workspace,
            )
        )

    def analyze(
        self,
        workspace: str | Path,
    ) -> dict:

        knowledge = (
            self.learn(
                workspace,
            )
        )

        return (
            self._summary_builder.build(
                knowledge,
            )
        )