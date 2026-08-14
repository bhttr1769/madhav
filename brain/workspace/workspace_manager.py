from pathlib import Path

from brain.workspace.workspace_learner import (
    WorkspaceLearner,
)

from brain.workspace.workspace_summary_builder import (
    WorkspaceSummaryBuilder,
)


class WorkspaceManager:
    """
    High-level entry point for workspace intelligence.
    """

    def __init__(
        self,
        learner: WorkspaceLearner,
    ):

        self._learner = learner

        self._summary_builder = (
            WorkspaceSummaryBuilder()
        )

    def analyze(
        self,
        workspace: str | Path,
    ) -> dict:

        knowledge = (
            self._learner.learn(
                workspace,
            )
        )

        return (
            self._summary_builder.build(
                knowledge,
            )
        )