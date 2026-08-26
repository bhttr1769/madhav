from dataclasses import dataclass


@dataclass(frozen=True)
class WorkspaceContext:
    """
    Represents interpreted workspace context.
    """

    workspace_type: str

    scale: str

    primary_technology: str | None

    primary_architecture: str | None

    confidence: float