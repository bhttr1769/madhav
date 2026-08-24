from brain.knowledge.builders.graph_builder import (
    GraphBuilder,
)

from brain.knowledge.models.edge_type import (
    EdgeType,
)

from brain.knowledge.models.node_type import (
    NodeType,
)

from brain.knowledge.stores.graph_store import (
    GraphStore,
)

from brain.workspace.models.workspace import (
    Workspace,
)


class WorkspaceKnowledgeBuilder:
    """
    Converts Workspace knowledge into the
    knowledge graph representation.
    """

    def __init__(
        self,
        builder: GraphBuilder,
    ):

        self._builder = builder

    def build(
        self,
        workspace: Workspace,
    ) -> GraphStore:

        repository = workspace.repository

        workspace_node = (
            self._builder.add_node(
                node_type=NodeType.PROJECT,
                name="Workspace",
                properties={
                    "files": repository.files,
                    "directories": repository.directories,
                },
                metadata={
                    "source": "workspace",
                },
                node_id="workspace",
            )
        )

        self._build_signatures(
            workspace_node.id,
            workspace,
        )

        self._build_technologies(
            workspace_node.id,
            workspace,
        )

        self._build_dependencies(
            workspace_node.id,
            workspace,
        )

        self._build_architectures(
            workspace_node.id,
            workspace,
        )

        return self._get_store()

    def _build_signatures(
        self,
        workspace_id: str,
        workspace: Workspace,
    ) -> None:

        for signature in (
            workspace.repository.signatures
        ):

            if signature.category == "filename":

                node_type = NodeType.FILE

            elif (
                signature.category
                == "directory"
            ):

                node_type = NodeType.DIRECTORY

            else:

                continue

            node_id = (
                f"{signature.category}:"
                f"{signature.path}"
            )

            node = (
                self._builder.add_node(
                    node_type=node_type,
                    name=signature.value,
                    properties={
                        "path": signature.path,
                    },
                    metadata={
                        "source": (
                            "workspace"
                        ),
                        "category": (
                            signature.category
                        ),
                    },
                    node_id=node_id,
                )
            )

            self._builder.add_edge(
                source_id=workspace_id,
                target_id=node.id,
                edge_type=(
                    EdgeType.CONTAINS
                ),
                metadata={
                    "source": (
                        "workspace"
                    ),
                },
            )

    def _build_technologies(
        self,
        workspace_id: str,
        workspace: Workspace,
    ) -> None:

        for technology in (
            workspace.technologies
        ):

            node_id = (
                f"technology:"
                f"{technology.name}"
            )

            node = (
                self._builder.add_node(
                    node_type=(
                        NodeType.TECHNOLOGY
                    ),
                    name=technology.name,
                    properties={
                        "category": (
                            technology.category
                        ),
                    },
                    metadata={
                        "source": (
                            "workspace"
                        ),
                    },
                    node_id=node_id,
                )
            )

            self._builder.add_edge(
                source_id=workspace_id,
                target_id=node.id,
                edge_type=EdgeType.USES,
                metadata={
                    "source": (
                        "workspace"
                    ),
                },
            )

    def _build_dependencies(
        self,
        workspace_id: str,
        workspace: Workspace,
    ) -> None:

        for dependency in (
            workspace.dependencies
        ):

            node_id = (
                f"dependency:"
                f"{dependency.name}"
            )

            node = (
                self._builder.add_node(
                    node_type=(
                        NodeType.DEPENDENCY
                    ),
                    name=dependency.name,
                    properties={},
                    metadata={
                        "source": (
                            "workspace"
                        ),
                    },
                    node_id=node_id,
                )
            )

            self._builder.add_edge(
                source_id=workspace_id,
                target_id=node.id,
                edge_type=(
                    EdgeType.DEPENDS_ON
                ),
                metadata={
                    "source": (
                        "workspace"
                    ),
                },
            )

    def _build_architectures(
        self,
        workspace_id: str,
        workspace: Workspace,
    ) -> None:

        for architecture in (
            workspace.architectures
        ):

            node_id = (
                f"architecture:"
                f"{architecture.name}"
            )

            node = (
                self._builder.add_node(
                    node_type=(
                        NodeType.ARCHITECTURE
                    ),
                    name=architecture.name,
                    properties={},
                    metadata={
                        "source": (
                            "workspace"
                        ),
                    },
                    node_id=node_id,
                )
            )

            self._builder.add_edge(
                source_id=workspace_id,
                target_id=node.id,
                edge_type=(
                    EdgeType.BUILT_WITH
                ),
                metadata={
                    "source": (
                        "workspace"
                    ),
                },
            )

    def _get_store(
        self,
    ) -> GraphStore:

        return self._builder._store