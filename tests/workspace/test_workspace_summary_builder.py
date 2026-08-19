from brain.workspace.models.architecture import (
    Architecture,
)
from brain.workspace.models.dependency import (
    Dependency,
)
from brain.workspace.models.repository import (
    Repository,
)
from brain.workspace.models.signature import (
    Signature,
)
from brain.workspace.models.technology import (
    Technology,
)
from brain.workspace.models.workspace import (
    Workspace,
)

from brain.workspace.workspace_summary_builder import (
    WorkspaceSummaryBuilder,
)


def test_workspace_summary_builder():

    workspace = Workspace(
        repository=Repository(
            files=2,
            directories=1,
            signatures={
                Signature(
                    value="main.py",
                    category="filename",
                    path="main.py",
                )
            },
        ),
        technologies={
            Technology(
                name="Python",
                category="language",
            )
        },
        dependencies={
            Dependency(
                name="pytest",
            )
        },
        architectures={
            Architecture(
                name="Layered",
            )
        },
    )

    summary = (
        WorkspaceSummaryBuilder()
    ).build(
        workspace,
    )

    assert (
        summary["files"]
        == 2
    )

    assert (
        summary["directories"]
        == 1
    )

    assert (
        summary["technologies"]
        == {"Python"}
    )

    assert (
        summary["dependencies"]
        == {"pytest"}
    )

    assert (
        summary["architectures"]
        == {"Layered"}
    )