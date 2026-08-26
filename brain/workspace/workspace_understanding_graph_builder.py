from brain.graph.storage.graph_store import (
    GraphStore,
)

from brain.graph.models.node import (
    Node,
)

from brain.graph.models.edge import (
    Edge,
)

from brain.workspace.models.workspace_context import (
    WorkspaceContext,
)

from brain.workspace.models.workspace_understanding import (
    WorkspaceUnderstanding,
)


class WorkspaceUnderstandingGraphBuilder:
    """
    Converts synthesized workspace understanding
    and context into graph knowledge.
    """

    def build(
        self,
        understanding: WorkspaceUnderstanding,
        context: WorkspaceContext,
    ) -> GraphStore:

        graph = GraphStore()

        workspace_id = "workspace"

        graph.add_node(
            Node(
                id=workspace_id,
                name=understanding.name,
                type="workspace",
                metadata={
                    "root": understanding.root,
                    "files": understanding.files,
                    "directories": understanding.directories,
                },
            )
        )

        context_id = "workspace-context"

        graph.add_node(
            Node(
                id=context_id,
                name="Workspace Context",
                type="workspace_context",
                metadata={
                    "workspace_type": (
                        context.workspace_type
                    ),
                    "scale": context.scale,
                    "primary_technology": (
                        context.primary_technology
                    ),
                    "primary_architecture": (
                        context.primary_architecture
                    ),
                    "confidence": context.confidence,
                },
            )
        )

        graph.add_edge(
            Edge(
                id="workspace-context",
                source=workspace_id,
                target=context_id,
                relation="has_context",
            )
        )

        self._add_technologies(
            graph,
            workspace_id,
            understanding,
        )

        self._add_dependencies(
            graph,
            workspace_id,
            understanding,
        )

        self._add_architectures(
            graph,
            workspace_id,
            understanding,
        )

        return graph

    def _add_technologies(
        self,
        graph: GraphStore,
        workspace_id: str,
        understanding: WorkspaceUnderstanding,
    ) -> None:

        for technology in understanding.technologies:

            node_id = (
                f"technology:{technology}"
            )

            graph.add_node(
                Node(
                    id=node_id,
                    name=technology,
                    type="technology",
                )
            )

            graph.add_edge(
                Edge(
                    id=(
                        f"workspace-uses-"
                        f"{technology}"
                    ),
                    source=workspace_id,
                    target=node_id,
                    relation="uses",
                )
            )

    def _add_dependencies(
        self,
        graph: GraphStore,
        workspace_id: str,
        understanding: WorkspaceUnderstanding,
    ) -> None:

        for dependency in understanding.dependencies:

            node_id = (
                f"dependency:{dependency}"
            )

            graph.add_node(
                Node(
                    id=node_id,
                    name=dependency,
                    type="dependency",
                )
            )

            graph.add_edge(
                Edge(
                    id=(
                        f"workspace-depends-"
                        f"{dependency}"
                    ),
                    source=workspace_id,
                    target=node_id,
                    relation="depends_on",
                )
            )

    def _add_architectures(
        self,
        graph: GraphStore,
        workspace_id: str,
        understanding: WorkspaceUnderstanding,
    ) -> None:

        for architecture in understanding.architectures:

            node_id = (
                f"architecture:{architecture}"
            )

            graph.add_node(
                Node(
                    id=node_id,
                    name=architecture,
                    type="architecture",
                )
            )

            graph.add_edge(
                Edge(
                    id=(
                        f"workspace-follows-"
                        f"{architecture}"
                    ),
                    source=workspace_id,
                    target=node_id,
                    relation="follows",
                )
            )