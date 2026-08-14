from brain.workspace.models.workspace import (
    Workspace,
)


class WorkspaceSummaryBuilder:
    """
    Builds a serializable workspace summary.
    """

    def build(
        self,
        workspace: Workspace,
    ) -> dict:

        return {
            "files": (
                workspace.repository.files
            ),
            "directories": (
                workspace.repository.directories
            ),
            "technologies": {
                technology.name
                for technology
                in workspace.technologies
            },
            "dependencies": {
                dependency.name
                for dependency
                in workspace.dependencies
            },
            "architectures": {
                architecture.name
                for architecture
                in workspace.architectures
            },
        }