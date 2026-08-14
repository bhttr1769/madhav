from brain.graph.storage.graph_store import (
    GraphStore,
)

from brain.graph.models.node import (
    Node,
)

from brain.graph.models.edge import (
    Edge,
)

from brain.workspace.models.workspace import (
    Workspace,
)


class WorkspaceGraphBuilder:
    """
    Converts a workspace into graph knowledge.
    """

    def build(
        self,
        workspace: Workspace,
    ) -> GraphStore:

        graph = GraphStore()

        project = Node(
            id="workspace",
            name="Workspace",
            type="workspace",
        )

        graph.add_node(
            project,
        )

        for technology in workspace.technologies:

            node = Node(
                id=technology.name,
                name=technology.name,
                type=technology.category,
            )

            graph.add_node(
                node,
            )

            graph.add_edge(
                Edge(
                    id=f"uses-{technology.name}",
                    source="workspace",
                    target=technology.name,
                    relation="uses",
                )
            )

        for dependency in workspace.dependencies:

            node = Node(
                id=dependency.name,
                name=dependency.name,
                type="dependency",
            )

            graph.add_node(
                node,
            )

            graph.add_edge(
                Edge(
                    id=f"depends-{dependency.name}",
                    source="workspace",
                    target=dependency.name,
                    relation="depends_on",
                )
            )

        for architecture in workspace.architectures:

            node = Node(
                id=architecture.name,
                name=architecture.name,
                type="architecture",
            )

            graph.add_node(
                node,
            )

            graph.add_edge(
                Edge(
                    id=f"follows-{architecture.name}",
                    source="workspace",
                    target=architecture.name,
                    relation="follows",
                )
            )

        return graph