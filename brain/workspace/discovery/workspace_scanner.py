from pathlib import Path


class WorkspaceScanner:
    """
    Recursively scans an entire workspace.
    """

    def scan(
        self,
        workspace: str | Path,
    ) -> list[Path]:

        workspace = Path(workspace)

        return [
            path
            for path in workspace.rglob("*")
            if path.is_file()
        ]