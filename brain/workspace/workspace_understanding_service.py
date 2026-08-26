from pathlib import Path

from brain.workspace.models.workspace import (
    Workspace,
)

from brain.workspace.models.workspace_understanding import (
    WorkspaceUnderstanding,
)


class WorkspaceUnderstandingService:
    """
    Synthesizes workspace-level understanding.
    """

    def analyze(
        self,
        workspace: Workspace,
        root: str | Path,
        name: str | None = None,
    ) -> WorkspaceUnderstanding:

        root_path = Path(
            root
        ).resolve()

        workspace_name = (
            name
            if name is not None
            else root_path.name
        )

        return WorkspaceUnderstanding(
            name=workspace_name,
            root=str(root_path),
            files=workspace.repository.files,
            directories=workspace.repository.directories,
            technologies=frozenset(
                technology.name
                for technology
                in workspace.technologies
            ),
            dependencies=frozenset(
                dependency.name
                for dependency
                in workspace.dependencies
            ),
            architectures=frozenset(
                architecture.name
                for architecture
                in workspace.architectures
            ),
        )