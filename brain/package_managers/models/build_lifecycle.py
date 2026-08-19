from dataclasses import dataclass

from brain.package_managers.models.project_commands import (
    ProjectCommand,
)


@dataclass(
    frozen=True,
)
class BuildLifecycle:
    """
    Represents a project's build workflow.
    """

    commands: frozenset[
        ProjectCommand
    ]