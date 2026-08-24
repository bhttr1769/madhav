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

from brain.package_managers.models.package_manager_environment import (
    PackageManagerEnvironment,
)


class PackageManagerKnowledgeBuilder:
    """
    Converts package-manager knowledge into
    knowledge graph nodes and relationships.
    """

    def __init__(
        self,
        builder: GraphBuilder,
    ):

        self._builder = builder

    def build(
        self,
        environment: PackageManagerEnvironment,
        workspace_id: str = "workspace",
    ) -> GraphStore:

        self._ensure_workspace(
            workspace_id,
        )

        self._build_managers(
            workspace_id,
            environment,
        )

        self._build_dependency_files(
            workspace_id,
            environment,
        )

        self._build_dependencies(
            workspace_id,
            environment,
        )

        self._build_lifecycles(
            workspace_id,
            environment,
        )

        return self._builder._store

    def _ensure_workspace(
        self,
        workspace_id: str,
    ) -> None:

        if (
            self._builder._store.get_node(
                workspace_id,
            )
            is None
        ):

            self._builder.add_node(
                node_type=NodeType.PROJECT,
                name="Workspace",
                metadata={
                    "source": "package_manager",
                },
                node_id=workspace_id,
            )

    def _build_managers(
        self,
        workspace_id: str,
        environment: PackageManagerEnvironment,
    ) -> None:

        for manager in environment.managers:

            node_id = (
                f"package-manager:"
                f"{manager.name}"
            )

            node = (
                self._builder.add_node(
                    node_type=NodeType.PACKAGE,
                    name=manager.name,
                    properties={
                        "manifest": (
                            manager.manifest
                        ),
                    },
                    metadata={
                        "source": (
                            "package_manager"
                        ),
                        "entity": (
                            "package_manager"
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
                        "package_manager"
                    ),
                },
            )

    def _build_dependency_files(
        self,
        workspace_id: str,
        environment: PackageManagerEnvironment,
    ) -> None:

        for dependency_file in (
            environment.dependency_files
        ):

            node_id = (
                f"dependency-file:"
                f"{dependency_file.path}"
            )

            node = (
                self._builder.add_node(
                    node_type=NodeType.FILE,
                    name=dependency_file.name,
                    properties={
                        "path": (
                            dependency_file.path
                        ),
                        "type": (
                            dependency_file.type
                        ),
                    },
                    metadata={
                        "source": (
                            "package_manager"
                        ),
                        "entity": (
                            "dependency_file"
                        ),
                    },
                    node_id=node_id,
                )
            )

            self._builder.add_edge(
                source_id=workspace_id,
                target_id=node.id,
                edge_type=EdgeType.CONTAINS,
                metadata={
                    "source": (
                        "package_manager"
                    ),
                },
            )

    def _build_dependencies(
        self,
        workspace_id: str,
        environment: PackageManagerEnvironment,
    ) -> None:

        for dependency in (
            environment.dependencies
        ):

            node_id = (
                f"package-dependency:"
                f"{dependency.name}:"
                f"{dependency.version}:"
                f"{dependency.source}"
            )

            metadata = dict(
                dependency.metadata
            )

            node = (
                self._builder.add_node(
                    node_type=NodeType.DEPENDENCY,
                    name=dependency.name,
                    properties={
                        "version": (
                            dependency.version
                        ),
                        "source": (
                            dependency.source
                        ),
                    },
                    metadata={
                        "source": (
                            "package_manager"
                        ),
                        "entity": (
                            "dependency"
                        ),
                        **metadata,
                    },
                    node_id=node_id,
                )
            )

            self._builder.add_edge(
                source_id=workspace_id,
                target_id=node.id,
                edge_type=EdgeType.DEPENDS_ON,
                metadata={
                    "source": (
                        "package_manager"
                    ),
                },
            )

    def _build_lifecycles(
        self,
        workspace_id: str,
        environment: PackageManagerEnvironment,
    ) -> None:

        for index, lifecycle in enumerate(
            environment.lifecycles
        ):

            node_id = (
                f"build-lifecycle:{index}"
            )

            commands = [
                {
                    "name": command.name,
                    "command": command.command,
                }
                for command in lifecycle.commands
            ]

            node = (
                self._builder.add_node(
                    node_type=NodeType.ARCHITECTURE,
                    name=(
                        f"Build Lifecycle "
                        f"{index + 1}"
                    ),
                    properties={
                        "commands": commands,
                    },
                    metadata={
                        "source": (
                            "package_manager"
                        ),
                        "entity": (
                            "build_lifecycle"
                        ),
                    },
                    node_id=node_id,
                )
            )

            self._builder.add_edge(
                source_id=workspace_id,
                target_id=node.id,
                edge_type=EdgeType.BUILT_WITH,
                metadata={
                    "source": (
                        "package_manager"
                    ),
                },
            )