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

from brain.workspace.workspace_graph_builder import (
    WorkspaceGraphBuilder,
)


def test_workspace_graph_builder():

    workspace = Workspace(
        repository=Repository(
            files=1,
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

    graph = (
        WorkspaceGraphBuilder()
    ).build(
        workspace,
    )

    assert (
        len(
            graph.graph.nodes
        )
        == 4
    )

    assert (
        len(
            graph.graph.edges
        )
        == 3
    )